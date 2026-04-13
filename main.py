#!/usr/bin/env python3
"""
iPhone Error 4030 Diagnostic & Repair Tool

Strumento diagnostico per risolvere l'errore 4030 durante il restore iOS.
Usa irecovery (libimobiledevice) per il rilevamento e pymobiledevice3/idevicerestore per il restore.
"""

import sys
import subprocess
import time
import json
import shutil
from pathlib import Path

PYTHON = sys.executable
PMD3 = [PYTHON, "-m", "pymobiledevice3"]

IPSW_API = "https://api.ipsw.me/v4/device/"


def run(args: list[str], timeout: int = 30) -> tuple[int, str, str]:
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -1, "", str(e)


def header(msg: str):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}\n")


def step(num: int, msg: str):
    print(f"\n[STEP {num}] {msg}")
    print("-" * 40)


def ok(msg: str):
    print(f"  \u2713 {msg}")


def warn(msg: str):
    print(f"  \u26a0 {msg}")


def fail(msg: str):
    print(f"  \u2717 {msg}")


def info(msg: str):
    print(f"  \u2192 {msg}")


# ─── Step 1: Detect device via irecovery ─────────────────────────────────

def detect_device() -> dict | None:
    """Rileva dispositivo in qualsiasi modalità."""
    step(1, "Rilevamento dispositivo")

    # Prima prova irecovery (funziona in Recovery e DFU)
    device = detect_via_irecovery()
    if device:
        return device

    # Prova modalità normale via usbmux
    device = detect_via_usbmux()
    if device:
        return device

    fail("Nessun dispositivo rilevato!")
    print()
    print("  Assicurati che:")
    print("  1. Il cavo USB sia collegato direttamente (no hub)")
    print("  2. Preferisci USB-A over USB-C se possibile")
    print("  3. Il dispositivo sia acceso o in Recovery/DFU")
    print()
    print("  Per entrare in Recovery mode (iPhone 8+):")
    print("  1. Volume Su (rapido)")
    print("  2. Volume Giu' (rapido)")
    print("  3. Tieni Side button finche' appare schermata Recovery")
    return None


def detect_via_irecovery() -> dict | None:
    """Rileva dispositivo via irecovery (Recovery/DFU mode)."""
    if not shutil.which("irecovery"):
        warn("irecovery non installato (brew install libirecovery)")
        return None

    code, out, err = run(["irecovery", "-q"], timeout=10)
    if code != 0:
        return None

    data = {}
    for line in out.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            data[key.strip()] = val.strip()

    mode = data.get("MODE", "Unknown")
    name = data.get("NAME", "Unknown")
    product = data.get("PRODUCT", "Unknown")
    ecid = data.get("ECID", "N/A")
    serial = data.get("SRNM", "N/A")
    nonce = data.get("NONC", "N/A")

    ok(f"Dispositivo trovato: {name}")
    info(f"Modalita': {mode}")
    info(f"Prodotto: {product}")
    info(f"ECID: {ecid}")
    info(f"Seriale: {serial}")
    info(f"AP Nonce: {nonce[:32]}..." if len(nonce) > 32 else f"AP Nonce: {nonce}")
    info(f"Chip: CPID {data.get('CPID', 'N/A')}")

    return {
        "mode": mode.lower(),
        "name": name,
        "product": product,
        "ecid": ecid,
        "serial": serial,
        "nonce": nonce,
        "cpid": data.get("CPID", ""),
        "raw": data,
    }


def detect_via_usbmux() -> dict | None:
    """Rileva dispositivo in modalita' normale via usbmux."""
    code, out, err = run(PMD3 + ["usbmux", "list", "--usb", "--no-color"])
    if code != 0 or not out or out == "[]":
        return None

    try:
        devices = json.loads(out)
        if not devices:
            return None
        d = devices[0]
        udid = d.get("UniqueDeviceID", d.get("SerialNumber", "N/A"))
        ok(f"Dispositivo trovato in modalita' NORMALE (usbmux)")
        info(f"UDID: {udid}")
        return {"mode": "normal", "data": d, "udid": udid}
    except json.JSONDecodeError:
        return None


# ─── Step 2: USB diagnostics ─────────────────────────────────────────────

def diagnose_usb():
    """Verifica la qualita' della connessione USB."""
    step(2, "Diagnostica connessione USB")

    code, out, err = run(["system_profiler", "SPUSBDataType"], timeout=15)
    if code != 0 or not out:
        warn("Impossibile leggere i dati USB dal sistema")
        return

    lines = out.lower()

    if "usb 3" in lines or "superspeed" in lines:
        ok("Connessione USB 3.x (SuperSpeed) rilevata")
    elif "usb 2" in lines or "high-speed" in lines:
        ok("Connessione USB 2.0 (High-Speed) rilevata")
    else:
        warn("Tipo di connessione USB non determinato")

    if "hub" in lines:
        warn("Hub USB rilevato! Per errore 4030, collega DIRETTAMENTE al Mac")
    else:
        ok("Nessun hub USB nella catena")

    print()
    info("Suggerimenti USB per errore 4030:")
    print("  - Usa un cavo USB-A (piu' stabile di USB-C)")
    print("  - Prova una porta USB diversa")
    print("  - Evita prolunghe e adattatori")


# ─── Step 3: Firmware info ────────────────────────────────────────────────

def get_signed_ipsw(product: str) -> list[dict]:
    """Interroga ipsw.me per i firmware firmati."""
    try:
        import requests
    except ImportError:
        code, out, err = run(
            [PYTHON, "-c", f"import urllib.request, json; "
             f"r = urllib.request.urlopen('{IPSW_API}{product}?type=ipsw'); "
             f"d = json.loads(r.read()); "
             f"print(json.dumps([f for f in d.get('firmwares',[]) if f.get('signed')]))"],
            timeout=30
        )
        if code == 0 and out:
            return json.loads(out)
        return []

    resp = __import__("requests").get(
        f"{IPSW_API}{product}?type=ipsw",
        headers={"Accept": "application/json"},
        timeout=20
    )
    data = resp.json()
    return [fw for fw in data.get("firmwares", []) if fw.get("signed")]


def check_firmware(product: str = "iPhone12,3") -> str | None:
    """Verifica firmware firmati e ritorna URL del piu' recente."""
    step(3, f"Firmware firmati per {product}")

    signed = get_signed_ipsw(product)
    if not signed:
        fail("Nessun firmware firmato trovato!")
        return None

    for fw in signed:
        ok(f"iOS {fw['version']} (build {fw['buildid']}) — FIRMATO")
        info(f"  {fw['url']}")

    best = signed[0]
    print()
    info(f"Firmware consigliato: iOS {best['version']}")
    return best["url"]


# ─── Step 4: Mode switching ──────────────────────────────────────────────

def exit_recovery() -> bool:
    """Esce da Recovery/DFU."""
    step(4, "Uscita da Recovery/DFU")

    # Prova irecovery prima (piu' affidabile)
    if shutil.which("irecovery"):
        info("Invio comando di uscita via irecovery...")
        code, out, err = run(["irecovery", "-n"], timeout=10)
        if code == 0:
            ok("Comando di uscita inviato")
            info("Attendi 10-15 secondi per il riavvio...")
            time.sleep(5)
            return True

    # Fallback pymobiledevice3
    code, out, err = run(PMD3 + ["restore", "exit"], timeout=15)
    if code == 0:
        ok("Uscita Recovery via pymobiledevice3")
        time.sleep(5)
        return True

    warn(f"Uscita Recovery fallita")
    return False


def enter_recovery() -> bool:
    """Entra in Recovery mode."""
    info("Entro in Recovery mode...")
    code, out, err = run(PMD3 + ["restore", "enter"], timeout=15)
    if code == 0:
        ok("Dispositivo in Recovery mode")
        time.sleep(3)
        return True
    warn(f"Impossibile entrare in Recovery: {err or out}")
    return False


# ─── Step 5: Restore ─────────────────────────────────────────────────────

def attempt_restore(ipsw: str | None = None, erase: bool = True, use_idevicerestore: bool = False):
    """Tenta il restore. Prova prima idevicerestore, poi pymobiledevice3."""
    step(5, "Tentativo di restore")

    if use_idevicerestore and shutil.which("idevicerestore"):
        return restore_via_idevicerestore(ipsw, erase)
    return restore_via_pmd3(ipsw, erase)


def restore_via_idevicerestore(ipsw: str | None, erase: bool) -> bool:
    """Restore via idevicerestore (libimobiledevice)."""
    info("Uso idevicerestore (libimobiledevice)")

    args = ["idevicerestore", "-d", "-e"] if erase else ["idevicerestore", "-d"]
    if ipsw:
        args.append(ipsw)
    else:
        args.append("-l")  # latest signed

    info(f"Comando: {' '.join(args)}")
    return run_restore_process(args)


def restore_via_pmd3(ipsw: str | None, erase: bool) -> bool:
    """Restore via pymobiledevice3."""
    info("Uso pymobiledevice3")

    args = PMD3 + ["-v", "restore", "update"]
    if ipsw:
        args += ["-i", ipsw]
    if erase:
        args += ["--erase"]

    info(f"Modalita': {'ERASE (factory reset)' if erase else 'UPDATE'}")
    info(f"Comando: {' '.join(args)}")
    return run_restore_process(args)


def run_restore_process(args: list[str]) -> bool:
    """Esegue il processo di restore con output live e analisi."""
    print()
    print("  Avvio restore... (puo' richiedere 10-30 minuti)")
    print("  L'output mostra dove il processo si blocca.")
    print()

    try:
        process = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1
        )

        output_lines = []
        for line in process.stdout:
            line = line.rstrip()
            output_lines.append(line)
            print(f"  | {line}")

        process.wait(timeout=1800)

        if process.returncode == 0:
            ok("RESTORE COMPLETATO CON SUCCESSO!")
            return True

        fail(f"Restore fallito (exit code: {process.returncode})")
        analyze_restore_failure(output_lines)
        return False

    except subprocess.TimeoutExpired:
        process.kill()
        fail("Restore timeout dopo 30 minuti")
        return False
    except KeyboardInterrupt:
        process.kill()
        warn("Restore interrotto dall'utente")
        return False


def analyze_restore_failure(lines: list[str]):
    """Analizza l'output del restore fallito."""
    print()
    info("Analisi del fallimento:")
    full = "\n".join(lines).lower()

    checks = [
        (["sep"] , ["fail", "error"],
         "Fallimento fase SEP (Secure Enclave Processor)",
         "Prova un IPSW diverso o verifica il modello esatto"),
        (["baseband"], ["fail", "error"],
         "Fallimento fase Baseband",
         "Possibile problema hardware modem. Prova --ignore-fdr"),
        (["fdr"], ["fail", "error"],
         "Fallimento fase FDR (Factory Data Restore)",
         "Prova con --ignore-fdr"),
        (["usb"], ["timeout", "disconnect", "pipe"],
         "Disconnessione USB durante il restore",
         "Cambia cavo/porta USB, usa USB-A"),
        (["tss"], ["reject", "fail", "denied"],
         "Apple ha rifiutato la firma (TSS)",
         "Il firmware non e' piu' firmato. Scarica da ipsw.me"),
        (["nonce"], ["mismatch", "fail", "error"],
         "Problema con il nonce/APNonce",
         "Prova ciclo DFU->Recovery o nonce manuale"),
        (["4030", "error 40"], [],
         "Errore 4030 confermato",
         "1. Cambia cavo USB-A  2. Prova Recovery mode  3. Prova --erase"),
    ]

    matched = False
    for keywords, error_words, message, suggestion in checks:
        if any(kw in full for kw in keywords):
            if not error_words or any(ew in full for ew in error_words):
                fail(message)
                print(f"  \u2192 {suggestion}")
                matched = True
                break

    if not matched:
        warn("Causa specifica non identificata")

    meaningful = [l for l in lines if l.strip() and "progress" not in l.lower()]
    if meaningful:
        print()
        info("Ultime righe significative:")
        for line in meaningful[-5:]:
            print(f"    {line}")


# ─── Step 6: Recovery cycle strategy ─────────────────────────────────────

def recovery_cycle_strategy(ipsw: str | None = None):
    """Esci da DFU/Recovery -> rientra in Recovery -> restore."""
    step(6, "Strategia: ciclo DFU -> Recovery -> Restore")

    info("Fase 1: Uscita dal DFU/Recovery...")
    exit_recovery()
    time.sleep(8)

    info("Fase 2: Entrata in Recovery mode...")
    if enter_recovery():
        time.sleep(3)
        info("Fase 3: Restore da Recovery mode...")
        return attempt_restore(ipsw, erase=True)

    warn("Serve intervento manuale per entrare in Recovery")
    print()
    print("  iPhone 8+: Volume Su (rapido), Volume Giu' (rapido),")
    print("  tieni Side button finche' appare schermata Recovery")
    return False


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    header("iPhone Error 4030 — Diagnostic & Repair Tool")

    print("Diagnostica e risoluzione errore 4030 durante restore iOS.")
    print()

    ipsw_path = None
    for arg in sys.argv[1:]:
        if arg not in ("--auto", "--menu") and not arg.startswith("--"):
            p = Path(arg)
            if p.exists() and p.suffix == ".ipsw":
                ipsw_path = str(p)
                info(f"IPSW locale: {ipsw_path}")
            elif arg.startswith("http"):
                ipsw_path = arg
                info(f"IPSW URL: {arg[:80]}...")
            break

    if "--auto" in sys.argv:
        run_auto(ipsw_path)
    else:
        interactive_menu(ipsw_path)


def run_auto(ipsw: str | None = None):
    """Diagnostica automatica completa."""
    header("DIAGNOSTICA AUTOMATICA")

    # 1. Rileva
    device = detect_device()
    if not device:
        sys.exit(1)

    # 2. USB
    diagnose_usb()

    # 3. Firmware
    product = device.get("product", "iPhone12,3")
    if not ipsw:
        ipsw = check_firmware(product)

    mode = device.get("mode", "unknown")

    # 4. Restore strategy
    if mode == "recovery":
        info("\nDispositivo in Recovery — provo restore diretto con erase...")
        if not attempt_restore(ipsw, erase=True):
            info("\nFallito. Provo ciclo Recovery -> Normal -> Recovery...")
            recovery_cycle_strategy(ipsw)

    elif mode == "dfu":
        info("\nDispositivo in DFU — provo restore...")
        if not attempt_restore(ipsw, erase=True):
            info("\nFallito da DFU. Provo ciclo verso Recovery...")
            recovery_cycle_strategy(ipsw)

    else:
        info("\nDispositivo normale — entro in Recovery...")
        enter_recovery()
        time.sleep(3)
        attempt_restore(ipsw, erase=True)

    # Riepilogo
    header("DIAGNOSTICA COMPLETATA")
    print("Se non riuscito:")
    print("  1. Cavo USB-A diverso, collegato direttamente")
    print("  2. IPSW diverso (ipsw.me)")
    print("  3. Computer diverso")
    print()
    print("Se nulla funziona — possibile problema hardware:")
    print("  - Connettore Lightning danneggiato")
    print("  - Chip NAND difettoso")
    print("  - Problema scheda logica")


def interactive_menu(ipsw: str | None = None):
    """Menu interattivo."""
    device = None

    while True:
        print()
        print("+---------------------------------------------------+")
        print("|         MENU DIAGNOSTICA ERRORE 4030              |")
        print("+---------------------------------------------------+")
        print("|  1. Rileva dispositivo                            |")
        print("|  2. Diagnostica USB                               |")
        print("|  3. Firmware firmati (ipsw.me)                    |")
        print("|  4. Esci da Recovery/DFU                          |")
        print("|  5. Entra in Recovery mode                        |")
        print("|  6. Restore (erase) via pymobiledevice3           |")
        print("|  7. Restore (update) via pymobiledevice3          |")
        print("|  8. Restore (erase) via idevicerestore + DFU [*]  |")
        print("|  9. Ciclo DFU->Recovery->Restore                  |")
        print("| 10. Diagnostica automatica COMPLETA               |")
        print("|  0. Esci                                          |")
        print("+---------------------------------------------------+")
        print("  [*] = soluzione consigliata per errore 4030")

        if ipsw:
            name = ipsw if len(ipsw) < 60 else f"...{ipsw[-57:]}"
            print(f"  IPSW: {name}")

        choice = input("\n  Scelta [0-10]: ").strip()

        if choice == "1":
            device = detect_device()
        elif choice == "2":
            diagnose_usb()
        elif choice == "3":
            product = device.get("product", "iPhone12,3") if device else "iPhone12,3"
            url = check_firmware(product)
            if url and not ipsw:
                ipsw = url
                info(f"IPSW impostato automaticamente")
        elif choice == "4":
            exit_recovery()
        elif choice == "5":
            enter_recovery()
        elif choice == "6":
            attempt_restore(ipsw, erase=True, use_idevicerestore=False)
        elif choice == "7":
            attempt_restore(ipsw, erase=False, use_idevicerestore=False)
        elif choice == "8":
            attempt_restore(ipsw, erase=True, use_idevicerestore=True)
        elif choice == "9":
            recovery_cycle_strategy(ipsw)
        elif choice == "10":
            run_auto(ipsw)
        elif choice == "0":
            break
        else:
            print("  Scelta non valida")


if __name__ == "__main__":
    main()

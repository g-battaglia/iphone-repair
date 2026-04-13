# iOS Major Version Jump Restore Guide

A CLI tool and comprehensive guide for restoring an iPhone across major iOS version gaps (e.g., iOS 15 to iOS 26), resolving error 4030 and "image personalization failed" issues.

## The Problem

When attempting to restore an iPhone running a very old iOS version (e.g., 15.x) to a current version (e.g., 26.x), the restore fails with **error 4030** or **"image personalization failed"**. Standard methods (Finder, OTA update, Apple Configurator) all fail. Progressive updates (15 → 16 → 17 → ...) are impossible because Apple no longer signs intermediate versions.

## Root Cause

In **Recovery mode**, the device uses its own iBoot (from the currently installed iOS) to validate firmware components via IMG4 personalization. When the installed iOS is many major versions behind the target, the old iBoot cannot properly validate the new firmware format — it has changed too much over 11+ major versions.

## The Solution

Use **DFU mode** instead of Recovery mode. In DFU, the host tool loads a fresh iBSS and iBEC directly from the target IPSW, completely bypassing the device's old iBoot. This creates a new boot chain that knows how to handle the target firmware.

```bash
# The command that works (after entering DFU mode)
idevicerestore -d -e /path/to/firmware.ipsw
```

## Step-by-Step Process

This is the exact procedure that worked to restore an iPhone 11 Pro from iOS 15.3.1 to iOS 26.4.1. It applies to any iPhone stuck on an old iOS version where Finder/OTA/Apple Configurator fail with error 4030 or "image personalization failed".

### 1. Download the IPSW

Go to [ipsw.me](https://ipsw.me), find your device model, and download the latest signed IPSW. Do this **before** starting — the file is ~9GB and downloading during restore will cause timeouts.

### 2. Build idevicerestore from source

The Homebrew version may be outdated. Build from source for full DFU support:

```bash
# Clone and build the libimobiledevice stack
# A patched build script is included in tools/limd-build-patched.sh
# Or follow https://github.com/libimobiledevice/idevicerestore#building
```

Verify it works:
```bash
idevicerestore --version
irecovery --version
```

### 3. Put the iPhone in DFU mode

Connect the iPhone via USB (prefer USB-A, avoid hubs), then:

1. Press and quickly release **Volume Up**
2. Press and quickly release **Volume Down**
3. Press and hold **Side button** for 10 seconds (screen goes black)
4. While still holding Side, also press **Volume Down** for 5 seconds
5. Release Side button, keep holding Volume Down for 10 seconds

**If the screen stays black** → you're in DFU (correct).
**If the Apple/iTunes logo appears** → you're in Recovery (wrong — retry from step 1).

Verify:
```bash
irecovery -q
# Look for: MODE=DFU
```

### 4. Run the restore

```bash
idevicerestore -d -e /path/to/iPhone_26.4.1_Restore.ipsw
```

- `-d` = DFU mode
- `-e` = erase (full restore)

The process takes ~2 hours and goes through these phases:
1. **iBSS/iBEC** — fresh bootloaders loaded from IPSW (this is why DFU works)
2. **Firmware components** — SEP, baseband, ANE, AOP, and dozens more
3. **Filesystem** — main OS image flashed and verified
4. **Cryptex** — system security components (~2GB)
5. **Seal** — cryptographic signing of the system volume
6. **"Restore Finished"** — done

### 5. Setup

The iPhone reboots and shows the iOS setup screen. You're done.

### Why Recovery mode fails (and DFU works)

| | Recovery mode | DFU mode |
|---|---|---|
| Boot chain | Uses the device's **old iBoot** | Loads **fresh iBSS/iBEC** from the IPSW |
| Problem | Old iBoot can't validate new firmware | New boot chain handles everything |
| Result with large version gap | "image personalization failed" | Success |

See [wiki/root-cause.md](wiki/root-cause.md) and [wiki/dfu-vs-recovery.md](wiki/dfu-vs-recovery.md) for the full technical analysis.

---

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (package manager)
- [idevicerestore](https://github.com/libimobiledevice/idevicerestore) (build from source for DFU restore)
- [irecovery](https://github.com/libimobiledevice/libirecovery) (for device detection)

## Setup

```bash
uv sync
```

## Usage

### Interactive menu
```bash
uv run main.py
```

### Automatic diagnostics
```bash
uv run main.py --auto
```

### With a local IPSW file
```bash
uv run main.py /path/to/firmware.ipsw
```

## Features

- Device detection in Recovery, DFU, or normal mode
- USB connection diagnostics
- Signed firmware lookup via ipsw.me API
- Restore via idevicerestore (DFU/Recovery)
- Restore via pymobiledevice3
- Automatic restore failure analysis
- DFU → Recovery → Restore cycling

## Documentation

The `wiki/` directory contains detailed documentation of the entire diagnostic process, all attempts made, bugs encountered, and the final solution. See `wiki/index.md` for the full table of contents.

## Key Takeaway

**For iOS restores spanning many major versions, always use DFU mode.** Recovery mode relies on the device's installed iBoot, which may be incompatible with the target firmware. DFU mode loads a fresh boot chain from the IPSW, eliminating any version incompatibility.

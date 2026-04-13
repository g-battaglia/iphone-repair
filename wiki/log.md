# Log

## [2026-04-13] start | Project started
iPhone 11 Pro stuck on error 4030 after reset. Goal: diagnose and resolve autonomously. Device in Recovery mode, Finder detects it.

## [2026-04-13] attempt | Attempt 1 — pymobiledevice3 from Recovery
pymobiledevice3 restore update from Recovery mode. Failed: timeout during on-the-fly IPSW download, lockdownd connection lost.

## [2026-04-13] discovery | Device rebooted spontaneously
Phone restarted during operations. Strategy change: safe analysis without risk of re-reset.

## [2026-04-13] research | OTA and progressive update check
Confirmed: no OTA available from iOS 15 → 26. Only iOS 26.4.1 and 26.4 are signed. Progressive updates impossible.

## [2026-04-13] attempt | Attempt 2 — pymobiledevice3 with local IPSW
Downloaded 9.3GB IPSW locally. Failed: BrokenPipeError, unstable lockdownd connection.

## [2026-04-13] fix | IPSW saved permanently
IPSW moved to permanent path to avoid re-downloads and timeouts.

## [2026-04-13] attempt | Attempt 3 — pymobiledevice3 with pre-downloaded IPSW
Attempt with pre-downloaded local IPSW. Failed: "image personalization failed".

## [2026-04-13] fix | Disk space freed
Found two orphaned IPSW copies in temp dirs (16.4GB). Deleted, freed 9.3GB.

## [2026-04-13] build | Built idevicerestore from source
Built libimobiledevice, libirecovery, libtatsu, idevicerestore from source. Patched build script for non-interactive sudo.

## [2026-04-13] attempt | Attempt 4 — idevicerestore from Recovery
idevicerestore -e from Recovery mode. Failed: same "image personalization failed".

## [2026-04-13] research | Deep dive on error 4030
Found that DFU bypasses local iBoot, loads fresh boot chain. This could solve the old-iBoot/new-firmware incompatibility.

## [2026-04-13] milestone | Entered DFU mode
User put the device in DFU following guided procedure. Confirmed with `irecovery -q`: DFU mode.

## [2026-04-13] attempt | Attempt 5 — idevicerestore from DFU (SUCCESS)
`idevicerestore -d -e <ipsw>` from DFU mode. All phases completed:
- iBSS/iBEC personalized and sent
- All firmware components delivered
- Restore ramdisk booted, "restored" service connected
- Main filesystem flashed and verified (100%)
- Cryptex1 (SystemOS 2GB, SystemVolume, SystemTrustCache)
- System Volume sealed
- **"Restore Finished" — SUCCESS**

## [2026-04-13] documentation | Wiki created
Complete documentation of all attempts, findings, bugs, and solution in LLM Wiki format.

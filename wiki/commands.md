---
tags: [reference, commands, cli]
date: 2026-04-13
type: reference
---

# Key Commands

## Device detection
```bash
# Query device state in Recovery/DFU
irecovery -q

# List USB devices via usbmuxd
pymobiledevice3 usbmux list
```

## Restore
```bash
# Restore from DFU (THE COMMAND THAT WORKED)
idevicerestore -d -e /path/to/firmware.ipsw

# Restore from Recovery (failed in our case)
idevicerestore -e /path/to/firmware.ipsw

# Restore via pymobiledevice3
pymobiledevice3 restore update -i /path/to/firmware.ipsw
```

## Diagnostics
```bash
# Check Apple-signed versions for a device
pymobiledevice3 tss -d iPhone12,3

# Monitor restore output
tail -f /path/to/restore.log

# Verify USB connection
system_profiler SPUSBDataType
```

## Build idevicerestore from source
```bash
# Using the patched script
SUDO_ASKPASS=/path/to/askpass.sh bash tools/limd-build-patched.sh
```

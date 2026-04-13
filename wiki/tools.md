---
tags: [entity, tools, software]
date: 2026-04-13
type: entity
---

# Tools

## pymobiledevice3 (v9.9.1)
- **Source**: PyPI (`pip install pymobiledevice3`)
- **Use**: iOS restore via Python, device management
- **Issues encountered**: [[bug-pmd3-irecv-none]], unstable lockdownd connections, [[bug-ipsw-parser-posixpath]]
- **Result**: failed in all restore attempts (3 out of 3)

## idevicerestore (v1.0.0-270-g405fcd1)
- **Source**: built from GitHub sources (libimobiledevice)
- **Use**: low-level iOS restore, DFU support
- **Dependencies**: libirecovery 1.3.1, libtatsu 1.0.5-3-g60a39f3
- **Result**: failed from Recovery, **SUCCEEDED from DFU**
- **Build**: see [[bug-sudo-build]]

## irecovery (CLI)
- **Source**: built alongside libirecovery
- **Use**: communicate with devices in Recovery/DFU, detection
- **Key command**: `irecovery -q` to query device state

## IPSW
- **File**: `iPhone12,3,iPhone12,5_26.4.1_23E254_Restore.ipsw`
- **Size**: 9.3GB
- **Build**: 23E254 (iOS 26.4.1)
- **Variant used**: "Customer Erase Install (IPSW)"

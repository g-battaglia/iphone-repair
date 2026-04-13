---
tags: [attempt, failed, idevicerestore, recovery, image-personalization]
date: 2026-04-13
type: attempt
---

# Attempt 4 — idevicerestore from Recovery Mode

## Setup
- **Tool**: idevicerestore v1.0.0-270-g405fcd1 (built from source)
- **Mode**: Recovery mode
- **IPSW**: permanent local path

## Command
```bash
idevicerestore -e /path/to/iPhone12,3_26.4.1_23E254_Restore.ipsw
```

## Result: FAILED
- Same error: **"image personalization failed"**
- Confirmed that the problem is not the tool but the mode

## Analysis
With two different tools (pymobiledevice3 and idevicerestore) failing at the same point in Recovery mode, the problem is definitively in the device's boot chain, not in the host software.

This directed the research toward [[dfu-vs-recovery|DFU mode]] as the alternative.

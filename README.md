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

## How to Enter DFU Mode (iPhone 8 and later)

1. Press and quickly release **Volume Up**
2. Press and quickly release **Volume Down**
3. Press and hold **Side button** for 10 seconds (screen goes black)
4. While still holding Side button, also press **Volume Down** for 5 seconds
5. Release Side button, keep holding Volume Down for 10 seconds
6. If the screen stays black → you're in DFU. If the Apple logo appears → you're in Recovery (retry)

Verify with: `irecovery -q` (should show `MODE=DFU`)

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

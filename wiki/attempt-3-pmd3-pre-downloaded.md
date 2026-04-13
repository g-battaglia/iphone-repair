---
tags: [attempt, failed, pymobiledevice3, recovery, image-personalization]
date: 2026-04-13
type: attempt
---

# Attempt 3 — pymobiledevice3 with Pre-downloaded IPSW

## Setup
- **Tool**: pymobiledevice3 v9.9.1
- **Mode**: Recovery mode
- **IPSW**: pre-downloaded to a permanent project path

## Command
```bash
pymobiledevice3 restore update -i /path/to/iPhone12,3_26.4.1_23E254_Restore.ipsw
```

## Result: FAILED
- Error: **"image personalization failed"**
- The device received firmware components but couldn't validate them

## Analysis
This was the first signal that the problem was not USB or connectivity, but **the local iBoot**. The iOS 15.3.1 iBoot couldn't handle IMG4 personalization of iOS 26.4.1 components.

See [[root-cause]] for the full analysis.

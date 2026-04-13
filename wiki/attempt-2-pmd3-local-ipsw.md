---
tags: [attempt, failed, pymobiledevice3, recovery]
date: 2026-04-13
type: attempt
---

# Attempt 2 — pymobiledevice3 with Local IPSW

## Setup
- **Tool**: pymobiledevice3 v9.9.1
- **Mode**: Recovery mode
- **IPSW**: downloaded to a local temp path

## Command
```bash
pymobiledevice3 restore update -i /path/to/iPhone12,3_26.4.1_23E254_Restore.ipsw
```

## Result: FAILED
- BrokenPipeError during device communication
- The lockdownd connection dropped

## Analysis
Even with the IPSW local, the connection with the device in Recovery mode was unstable. The issue wasn't the download but the lockdownd session stability.

## Corrective action
IPSW moved to a permanent project path to avoid disk space issues and temp path problems. See also [[bug-disk-space]].

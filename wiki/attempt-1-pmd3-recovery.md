---
tags: [attempt, failed, pymobiledevice3, recovery]
date: 2026-04-13
type: attempt
---

# Attempt 1 — pymobiledevice3 from Recovery Mode

## Setup
- **Tool**: pymobiledevice3 v9.9.1
- **Mode**: Recovery mode
- **IPSW**: on-the-fly download from Apple CDN

## Command
```bash
pymobiledevice3 restore update
```

## Result: FAILED
- The tool started downloading the IPSW (9.3GB) from Apple CDN
- During the download (~15 minutes), the lockdownd connection with the device timed out
- Error: "waiting for device to connect for restored service"

## Analysis
The problem was that pymobiledevice3 downloaded the IPSW *during* the restore while keeping the USB connection alive. With 9.3GB to download, the timeout was inevitable.

## Lesson
Pre-download the IPSW before attempting the restore. See [[attempt-2-pmd3-local-ipsw]].

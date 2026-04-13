---
tags: [bug, pymobiledevice3, irecovery]
date: 2026-04-13
type: bug
---

# Bug: pymobiledevice3 Device() irecv=None

## Problem
The `Device()` class in pymobiledevice3 didn't automatically initialize the iRecovery binding, even though the device was in Recovery mode and `IRecv()` worked correctly.

## Impact
Unable to detect the device through pymobiledevice3's Python API for devices in Recovery mode.

## Fix
Used `irecovery -q` (CLI) directly for device detection in the diagnostic tool, bypassing the Python API.

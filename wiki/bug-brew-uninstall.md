---
tags: [bug, homebrew, dependencies]
date: 2026-04-13
type: bug
---

# Bug: brew uninstall Side Effect

## Problem
`brew uninstall --ignore-dependencies` to remove the Homebrew version of libimobiledevice also removed `ideviceinfo` and `irecovery`, which were used by other tools.

## Impact
All `irecovery`, `ideviceinfo`, etc. commands stopped working.

## Fix
Rebuilt everything from source:
- libimobiledevice
- libirecovery
- libtatsu
- idevicerestore

Source-built binaries were installed to `/usr/local/` and work independently of Homebrew.

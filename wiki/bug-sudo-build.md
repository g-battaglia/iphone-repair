---
tags: [bug, build, sudo, idevicerestore]
date: 2026-04-13
type: bug
---

# Bug: idevicerestore Build — Sudo Failures

## Problem
The libimobiledevice build script used `sudo make install` but there was no terminal available for password input (running from a non-interactive agent).

## Fix
1. Created an askpass helper script for non-interactive sudo
2. Patched the build script: `INSTALL_SUDO="sudo"` → `INSTALL_SUDO="sudo -A"`
3. Set `SUDO_ASKPASS` environment variable

## Patched file
`tools/limd-build-patched.sh`

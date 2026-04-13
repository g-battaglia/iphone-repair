---
tags: [bug, disk-space, ipsw]
date: 2026-04-13
type: bug
---

# Bug: Disk Space Exhaustion

## Problem
Two copies of the IPSW in temporary directories (9.3GB + 7.1GB) consumed almost all disk space, leaving only 4.1GB free.

## Cause
pymobiledevice3 downloaded the IPSW to temporary directories and didn't clean them up after restore failure.

## Fix
Deleted the orphaned temporary copy, freed 9.3GB. IPSW kept only in the permanent project path.

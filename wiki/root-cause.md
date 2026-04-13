---
tags: [analysis, root-cause, iboot, img4]
date: 2026-04-13
type: concept
---

# Root Cause Analysis

## The problem
Every restore attempt from Recovery mode failed with "image personalization failed".

## The cause
The **iOS 15.3.1 iBoot** could not properly validate **iOS 26.4.1** firmware components during IMG4 personalization.

### Why
- In Recovery mode, the device uses its own iBoot to orchestrate the restore
- The version gap was **11 major versions** (15 → 26)
- Over these years, Apple significantly evolved:
  - The IMG4 signature format
  - The TSS personalization protocol
  - Firmware component structure (Cryptex, Protected Volume, etc.)
- The old iBoot didn't know about these changes

### Evidence
- 4 attempts from Recovery mode: **all failed** at the same point (image personalization)
- 2 different tools (pymobiledevice3, idevicerestore): **same error**
- 1 attempt from DFU mode: **immediate success**
- This rules out USB, network, IPSW, or tool issues — the problem was iBoot

## The solution
[[dfu-vs-recovery|DFU mode]] completely bypasses the device's iBoot. The host loads fresh iBSS and iBEC from the iOS 26.4.1 IPSW, creating a boot chain that knows how to handle the new firmware.

## General rule
When the device has a very old iOS relative to the target, **DFU is mandatory**. Recovery mode only works for "close" updates (1-2 major versions).

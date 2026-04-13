---
tags: [concept, dfu, recovery, boot-chain, key-insight]
date: 2026-04-13
type: concept
---

# DFU vs Recovery Mode

This distinction was the key to solving the problem. See [[root-cause]].

## Recovery Mode
- The device uses its **own iBoot** (from the currently installed iOS version)
- The local iBoot handles IMG4 validation of firmware components
- The host tool (Finder, idevicerestore) sends firmware, but the local iBoot validates it
- **Limitation**: if the iBoot is too old, it may not understand new signature formats

## DFU Mode (Device Firmware Update)
- The device **does not use its own iBoot**
- The host loads **iBSS** (first-stage bootloader) directly from the target IPSW
- Then loads **iBEC** (second-stage bootloader) from the target IPSW
- The boot chain is **completely new**, coming from the target firmware
- No dependency on the currently installed firmware

## Comparison

| Aspect | Recovery | DFU |
|--------|----------|-----|
| Boot chain | Local iBoot | iBSS/iBEC from IPSW |
| Firmware validation | Old iBoot | Fresh boot chain |
| Cross-version compatibility | Limited | Full |
| Screen | iTunes/cable logo | Black (no video output) |
| How to enter | Vol+ > Vol- > Power 10s | Vol+ > Vol- > Power 10s > Vol- 5s |

## How to enter DFU (iPhone with Face ID)
1. Press and quickly release **Volume Up**
2. Press and quickly release **Volume Down**
3. Press and hold **Side button** for 10 seconds (screen goes black)
4. While still holding Side, also press **Volume Down** for 5 seconds
5. Release Side button, keep holding Volume Down for 10 seconds
6. If screen stays black = DFU. If Apple logo appears = Recovery (retry)

## Verification
```bash
irecovery -q
# In DFU: MODE=DFU
# In Recovery: MODE=Recovery
```

## Implication
For restores spanning many major versions, **always use DFU**. See [[lessons]].

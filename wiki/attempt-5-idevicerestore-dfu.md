---
tags: [attempt, success, idevicerestore, dfu, solution]
date: 2026-04-13
type: attempt
---

# Attempt 5 — idevicerestore from DFU Mode (SUCCESS)

## Setup
- **Tool**: idevicerestore v1.0.0-270-g405fcd1 (built from source)
- **Mode**: DFU mode
- **IPSW**: permanent local path
- **Variant**: Customer Erase Install (IPSW)

## Command
```bash
idevicerestore -d -e /path/to/iPhone12,3_26.4.1_23E254_Restore.ipsw
```

The `-d` flag indicates DFU mode.

## Result: SUCCESS

### Phases completed (in order)
1. **iBSS/iBEC**: personalized with SHSH blobs and sent to device
2. **Recovery Environment**: RestoreLogo, ANE, AOP, AVE2, Homer, multitouch, ISP, etc.
3. **SEP** (Secure Enclave Processor): firmware sent and activated
4. **Baseband**: TSS request, SHSH blobs received, firmware sent (with non-critical `mbn_stitch` warnings)
5. **Main filesystem**: sent and verified at 100%
6. **Unmount/Mount/Create Protected Volume**
7. **Cryptex1**: SystemOS (2GB), SystemVolume, SystemTrustCache
8. **SystemImageRootHash**: sent
9. **Seal System Volume**: cryptographic signing of the volume
10. **"Restore Finished" — DONE**

### Duration
~2 hours total from command start to "Restore Finished".

## Why it worked
See [[root-cause]]. In DFU, iBSS and iBEC are loaded from the iOS 26.4.1 IPSW, creating a completely new boot chain that knows how to handle the target firmware. The old iBoot (iOS 15.3.1) is completely bypassed.

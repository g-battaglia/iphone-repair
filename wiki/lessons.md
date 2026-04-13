---
tags: [lessons, best-practices, reference]
date: 2026-04-13
type: reference
---

# Lessons Learned

## 1. For major version jumps: use DFU, not Recovery
Recovery mode uses the iBoot installed on the device. If it's too old relative to the target firmware, IMG4 personalization will fail. DFU loads a completely new boot chain from the IPSW.

## 2. Always pre-download the IPSW
Don't let the tool download the IPSW during the restore. The USB/lockdownd connection can time out. Download the IPSW first, then pass the local path.

## 3. Progressive iOS updates are impossible
Apple only signs the latest versions. You can't do 15 → 16 → 17 → 18 → 26. The only option is a direct jump to the most recent signed version.

## 4. When one tool fails, try another
pymobiledevice3 and idevicerestore have different implementations of the same protocol. If one fails for non-obvious reasons, try the other before concluding the problem is unsolvable.

## 5. When the tool isn't the problem, change the mode
If two different tools fail at the same point, the problem isn't the tool. In our case, switching from Recovery to DFU solved everything.

## 6. Watch disk space with large IPSW files
An iOS IPSW is ~9GB. Tools like pymobiledevice3 may create temporary copies. Monitor disk space, especially on Macs with small SSDs.

## 7. Build from source when needed
Homebrew versions may be outdated or incompatible. Building libimobiledevice/idevicerestore from source gives access to the latest fixes and full debug output.

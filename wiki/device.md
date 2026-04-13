---
tags: [entity, iphone, hardware]
date: 2026-04-13
type: entity
---

# Device — iPhone 11 Pro

| Field | Value |
|-------|-------|
| Model | iPhone 11 Pro |
| Identifier | iPhone12,3 |
| Chip | A13 Bionic |
| CPID | 0x8030 |
| Board | d421ap |
| Image4 support | true |
| iOS pre-reset | 15.3.1 |
| iBoot version | mBoot-18000.102.4 |
| iOS post-restore | 26.4.1 (build 23E254) |

## Notes
- The device was working normally on iOS 15.3.1 before the reset
- After the reset, it got stuck on [[error-4030]]
- Restore completed successfully via [[dfu-vs-recovery|DFU mode]] + [[tools|idevicerestore]]

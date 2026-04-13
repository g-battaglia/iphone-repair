# Index

## Overview
- [[overview]] — Project summary: error 4030 on iPhone 11 Pro, resolved via DFU restore

## Concepts
- [[error-4030]] — Undocumented Apple restore error in the 40xx family
- [[dfu-vs-recovery]] — Why DFU mode was the key to solving the problem
- [[root-cause]] — Root cause analysis: old iBoot incompatible with new firmware
- [[ios-signing]] — Apple TSS/SHSH signing and why progressive updates are impossible

## Entities
- [[device]] — iPhone 11 Pro (iPhone12,3)
- [[tools]] — pymobiledevice3, idevicerestore, irecovery, versions

## Attempts (chronological)
- [[attempt-1-pmd3-recovery]] — pymobiledevice3 from Recovery, timeout during download
- [[attempt-2-pmd3-local-ipsw]] — pymobiledevice3 with local IPSW, BrokenPipeError
- [[attempt-3-pmd3-pre-downloaded]] — pymobiledevice3 with pre-downloaded IPSW, image personalization failed
- [[attempt-4-idevicerestore-recovery]] — idevicerestore from Recovery, image personalization failed
- [[attempt-5-idevicerestore-dfu]] — idevicerestore from DFU mode, SUCCESS

## Bugs & Fixes
- [[bug-pmd3-irecv-none]] — pymobiledevice3 Device() irecv=None
- [[bug-ipsw-parser-posixpath]] — ipsw_parser PosixPath .startswith() error
- [[bug-disk-space]] — Disk space exhaustion from duplicate IPSW copies
- [[bug-sudo-build]] — idevicerestore build sudo failures
- [[bug-brew-uninstall]] — brew uninstall side effect removing shared dependencies

## Reference
- [[commands]] — Key commands used throughout the process
- [[lessons]] — Lessons learned and recommendations

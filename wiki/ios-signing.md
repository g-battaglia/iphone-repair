---
tags: [concept, tss, shsh, signing, apple]
date: 2026-04-13
type: concept
---

# iOS Signing (TSS/SHSH)

## How it works
Apple controls which iOS versions can be installed on each device through the **TSS** (Tatsu Signing Server) system. During a restore, the host tool requests a **SHSH blob** (signed ticket) from Apple for each firmware component. Apple only signs versions it chooses to keep "open".

## Current status for iPhone12,3 (April 2026)
- **Signed**: iOS 26.4.1, iOS 26.4
- **Unsigned**: all previous versions (15.x, 16.x, 17.x, 18.x, 19.x-25.x)

## Implications
- **Progressive updates are impossible**: you can't do 15 → 16 → 17 → 18 → 26 because intermediate versions are unsigned
- **No OTA deltas available**: no OTA path from iOS 15 to intermediate versions
- **MDM/Apple Configurator**: also bound by TSS — they cannot install unsigned versions
- The only option is a direct jump from 15 to the latest signed version (26.4.1)

## IMG4 Personalization
Apple signs firmware components **per-device** using the ECID (unique chip identifier). This means:
- Each device gets different blobs
- Blobs are not transferable between devices
- Blobs expire when Apple stops signing that version

## Relation to [[error-4030]]
The TSS system was working correctly — Apple was signing iOS 26.4.1. The problem was that the local iBoot couldn't use those blobs to validate the components. See [[root-cause]].

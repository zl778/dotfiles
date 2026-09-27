# Official vendor equipment selection notes

Use this reference with the official-product evidence and OfficeCLI workflow. It records the recurring pattern, not a claim that the listed models are current forever.

## Evidence rules

- Search the named manufacturer's official domain first; open the exact product page or official datasheet, not just a search snippet or reseller page.
- Separate exact-model evidence from same-family evidence. Label each requirement `已明确满足`, `官网未列出`, `仅同系列证明`, or `存在偏差`.
- Do not upgrade vague specifications: `支持PoE` is not proof of `802.3at`; `告警2出` is not proof of `2路NO DC12V/20mA`; a thermal dual-spectrum camera is not an independent photoelectric smoke detector; an external siren is not a platform.
- If the user requires one brand throughout, treat brand continuity as a hard constraint. A cross-brand close match must be reported as a deviation, not silently substituted.
- For devices that only execute local output, map the whole chain: detector/analytics -> camera/NVR/controller/platform -> relay/output -> siren. Attribute APP push, video review, acknowledge, reset and logs to the component that actually provides them.

## Models encountered in the fire/network equipment workflow

- Uniview TIC-S2A32-IR@TP-F7-4F6-CA-VD2: close candidate for 400W-class thermal/visible-light safety camera; public evidence leaves items such as MJPEG, PoE 802.3at, NTC method and NO/DC12V/20mA alarm electrical details for confirmation.
- Uniview TIC-S2A32-IR@P-GW: same-family public specs are more complete, but public data showed PoE 802.3af and did not list MJPEG; do not present it as an unconditional match to a 802.3at/MJPEG requirement.
- Uniview NVR-B500-R16@128-B: practical recorder candidate with 16 SATA bays and capacity headroom; disclose that it exceeds an 8-bay minimum. For 19 streams at 4 Mbps for 90 days, theoretical storage is about 73.872 TB; capacity must be dimensioned with RAID/filesystem margin.
- Uniview NVR208-32: closer to a historical 32-channel/8-SATA requirement, but public capacity is insufficient for 19 x 4 Mbps continuous 90-day retention without changing the storage design.
- TP-LINK TL-MC200CM: 1.25Gbps SC multimode dual-fiber, 10/100/1000 RJ45, 850nm, 550m; suitable for a <=500m 6-core outdoor multimode link using two cores, with four spare cores. Confirm actual fiber core size and measured route length.
- H3C S5130S-20P-EI: exact 16 x 10/100/1000BASE-T + 4 x 1000BASE-X SFP + Console candidate; official Chinese specs list 336Gbps switching capacity and 114Mpps, with full-duplex support.
- UOZO/优周 ES603: official page identifies it as a sound-and-light siren, but public page does not expose complete electrical/environmental parameters. It can serve as a local output in a larger alarm chain; remote forwarding, APP/platform push, video verification, acknowledge/reset and log retention require the upstream controller/platform and must not be attributed to ES603 itself.

## Safe output pattern

Give the recommendation first, then a requirement/evidence matrix, official source URL, unresolved items, and a tender-ready wording that uses `待厂家确认/存在偏差` where evidence is incomplete. When editing an equipment list, preserve the original workbook and write a versioned sibling with OfficeCLI, then validate and re-read the edited cells.
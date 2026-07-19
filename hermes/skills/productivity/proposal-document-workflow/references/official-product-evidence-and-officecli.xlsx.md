# Official product evidence and OfficeCLI equipment-list workflow

## Evidence pattern from the Uniview camera check

Official pages reviewed:

- `https://cn.uniview.com/Products/Professional/Camera/7/` — `TIC-S2A32-IR@TP-F7-4F6-CA-VD2`, measurement thermal dual-spectrum bullet page.
- `https://cn.uniview.com/Products/Professional/Camera/TIC-S2A32-IR-P-GW/` — `TIC-S2A32-IR@P-GW`, detailed table page.
- `https://cn.uniview.com/Products/Professional/Camera/HIC2621-IR-B/` — `HIC2621-IR@IR9-B`, useful contrast model but only 2MP and not thermal.

The TP-F7-4F6-CA-VD2 page explicitly states: 400万 visible-light format, thermal measurement accuracy ±2℃ or ±2% (larger value), DC12V/PoE, alarm 2-in/2-out, thermal/visible-light linkage, and dual-spectrum operation. It does not, on the public page inspected, explicitly state MJPEG, PoE IEEE802.3at, NTC measurement, or the electrical details `NO/DC12V/20mA` for the two outputs.

The P-GW detailed page explicitly states: 400万, selectable 1920×1080, H.264 Baseline/Main/High Profile, three streams, 128Kbps–16384Kbps bitrate, 30fps maximum, thermal fire/smoke/temperature detection, linkage alarms, ONVIF/API/GB/T28181/GA/T1400, alarm 2-in/2-out, and measurement accuracy ±2℃ or ±2% (larger value). Its public page lists PoE `IEEE802.3af`, not `802.3at`, and does not list MJPEG or the NO/DC12V/20mA output electrical specification.

Therefore the correct conclusion is “closest candidate; unresolved items require exact-model datasheet or manufacturer written confirmation,” not “fully compliant.” `HIC2621-IR@IR9-B` confirms that some Uniview models support PoE `802.3af/802.3at`, H.264 High Profile, three streams, ONVIF and 1920×1080, but it is 200万 and not a thermal camera with two alarm outputs, so it is not a valid substitute.

## Evidence wording rules

- `支持PoE` ≠ `PoE 802.3at`.
- `告警输出2出` ≠ `2路NO、DC12V/20mA`.
- `测温精度±2℃或±2%` ≠ proof of `NTC` method unless NTC is stated.
- A family/similar-model page is not exact-model proof.
- For procurement or tender response, preserve a per-row status: `已明确满足`, `官网未列出`, `仅同系列证明`, or `存在偏差`.

## OfficeCLI equipment-list pattern

For a workbook whose header is `序、产品名称、品牌、数量、参数要求、型号、备注`:

1. Read the workbook to discover the real sheet name; do not assume `Sheet1`.
2. Copy the source to a versioned sibling and retain a `/tmp/` backup.
3. Use OfficeCLI batch updates against the exact parameter column (in the reviewed workbook this was `/Sheet1 (2)/E2:E29`).
4. Include requirements and unresolved conflicts in the cell text; do not silently rewrite the listed model or quantity.
5. Set `alignment.wrapText=true` and `alignment.vertical=top` on long requirement cells.
6. Run `officecli validate` and re-read the output workbook to verify all rows.

The checked workflow produced `设备清单_参数要求版.xlsx`, with 28 successful cell updates and `Validation passed: no errors found.`

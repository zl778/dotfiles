# Fire-device official evidence notes

## Selection rule

For tender equipment selection, distinguish three levels:

1. Exact-model official evidence: the manufacturer's detail page explicitly lists the required parameter.
2. Same-family/related-model evidence: useful for shortlisting only; it cannot be copied into the exact-model response.
3. Unresolved: the official page omits the parameter; require an exact-model datasheet, authorization, or written manufacturer confirmation.

Never convert a generic feature into a stricter electrical or protocol claim: `支持PoE` is not proof of `IEEE802.3at`; `告警2出` is not proof of `2路NO、DC12V/20mA`; a measurement accuracy value is not proof of an NTC method.

## Uniview thermal/fire camera shortlist

Official pages:

- `https://cn.uniview.com/Products/Professional/Camera/7/` — `TIC-S2A32-IR@TP-F7-4F6-CA-VD2`, measurement thermal dual-spectrum bullet page.
- `https://cn.uniview.com/Products/Professional/Camera/TIC-S2A32-IR-P-GW/` — `TIC-S2A32-IR@P-GW`, detailed table page.

The TP-F7-4F6-CA-VD2 page states 400万 visible-light format, thermal measurement accuracy ±2℃ or ±2% (larger value), DC12V/PoE, alarm 2-in/2-out, thermal/visible-light linkage, dual-spectrum operation, and industrial temperature measurement. It does not publicly state exact MJPEG support, PoE IEEE802.3at, NTC measurement, or the output electrical details NO/DC12V/20mA.

The P-GW detailed page states 400万, selectable 1920×1080, H.264 Baseline/Main/High Profile, three streams, 128Kbps–16384Kbps bitrate, 30fps maximum, thermal fire/smoke/temperature detection, linkage alarms, ONVIF/API/GB/T28181/GA/T1400, alarm 2-in/2-out, and ±2℃ or ±2% measurement accuracy. It lists PoE IEEE802.3af, not 802.3at, and does not list MJPEG or NO/DC12V/20mA output electrical parameters.

Conclusion: these are the closest public candidates, not fully proven matches. Ask Uniview for an exact-model confirmation of MJPEG, PoE 802.3at, NTC method, and 2-way NO/DC12V/20mA output before writing unconditional compliance.

## Uniview NVR shortlist

Official page:

- `https://cn.uniview.com/Products/Professional/NVR/NVR-B500-R16/` — `NVR-B500-R16@128-B`.

The page states 128 IPC inputs, 32×1080p@30 decoding, 1080P recording resolution, replay modes, recording/image/clip backup, intelligent search, 16 SATA bays, per-disk support up to 16TB, RAID0/1/5/6/10/50/60, alarm inputs/outputs, and AC100–240V input. It is a practical candidate when the requirement means at least 8 SATA bays; use 8×16TB and RAID5 as the capacity configuration, with the remaining bays reserved.

Capacity calculation for 19 channels × 4Mbps × 24h × 90 days:

- Daily data: 19 × 4Mbps ÷ 8 × 86400 = 820.8GB/day.
- 90-day theoretical requirement: 73,872GB ≈ 73.872TB.
- 8×16TB raw: 128TB.
- RAID5 theoretical usable capacity: approximately 112TB.
- Theoretical duration: approximately 136 days before filesystem/metadata/bitrate reserve.

The B500 page does not explicitly state the exact `50Hz±2%` range or third-party/ONVIF compatibility in the visible table; obtain written confirmation before final submission.

The older `NVR208-32` is an exact 32-channel/8-SATA family candidate and its official PDF states ONVIF compliance and 1080P@30 capability, but the official capacity is only about 32–48TB. That is below the 73.872TB theoretical requirement, so it cannot be accepted as a standalone 90-day solution without external storage or a changed bitrate/recording policy.

## Smoke detector candidate

Official page:

- `https://www.hikvision.com/cn/products/pdplist/69656/` — Hikvision `NP-FY300-4G`, independent photoelectric smoke/fire alarm detector.

The official page explicitly states:

- photoelectric detection principle;
- dual-optical sensing;
- real-time smoke detection/alarm and alarm information upload;
- 4G CAT1 communication;
- local alarm ≥85dB@3m (A-weighted);
- lithium-metal battery, average life 5 years;
- low-voltage, tamper, labyrinth contamination, and buzzer-fault alarms;
- self-test;
- sound/light alarm;
- DC3V supply;
- GB 20517-2006 compliance.

This is a much closer match than the available V1W sheet (RJ-45, ≥80dB@3m, >3 years). It is Hikvision rather than Uniview, so mixed-brand use requires authorization and confirmation of integration with the selected platform/DCS/alarm workflow. Do not silently replace a Uniview line item; record the brand/model substitution and obtain approval.

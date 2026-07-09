#!/usr/bin/env python3
"""
Merge two SRT subtitle files into a bilingual SRT.

Uses the primary language (first file) as the timeline and finds the best-
matching secondary-language segments via timestamp overlap. Output is a
single SRT where each segment shows both languages, one per line.

Usage:
    python3 merge_bilingual_subs.py primary.srt secondary.srt output.srt

Example:
    python3 merge_bilingual_subs.py video.en.srt video.zh-Hans.srt video.bilingual.srt
"""

import re
import sys


def parse_srt(filepath):
    """Parse an SRT file into a list of (index, start_sec, end_sec, text_lines)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.split(r'\n\n+', content.strip())
    entries = []

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue

        try:
            int(lines[0].strip())
        except ValueError:
            continue

        time_match = re.match(
            r'(\d{1,2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*'
            r'(\d{1,2}):(\d{2}):(\d{2})[,.](\d{3})',
            lines[1]
        )
        if not time_match:
            continue

        def to_sec(h, m, s, ms):
            return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

        start = to_sec(*[int(g) for g in time_match.groups()[:4]])
        end = to_sec(*[int(g) for g in time_match.groups()[4:]])

        text = '\n'.join(lines[2:]).strip()
        entries.append((start, end, text))

    entries.sort(key=lambda x: x[0])
    return entries


def format_time(seconds):
    """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def find_overlapping_secondary(pri_start, pri_end, secondary_entries):
    """Find secondary-language text segments overlapping a primary time range."""
    texts = []
    for zs, ze, txt in secondary_entries:
        overlap_start = max(pri_start, zs)
        overlap_end = min(pri_end, ze)
        if overlap_start < overlap_end:
            texts.append(txt)

    if not texts:
        return ""

    # Deduplicate while preserving order
    seen = set()
    unique = [t for t in texts if not (t in seen or seen.add(t))]
    return ' '.join(unique)


def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <primary.srt> <secondary.srt> <output.srt>",
              file=sys.stderr)
        sys.exit(1)

    pri_file, sec_file, out_file = sys.argv[1], sys.argv[2], sys.argv[3]

    pri_entries = parse_srt(pri_file)
    sec_entries = parse_srt(sec_file)

    print(f"Primary:   {len(pri_entries)} segments", file=sys.stderr)
    print(f"Secondary: {len(sec_entries)} segments", file=sys.stderr)

    out_lines = []
    srt_idx = 1

    for pri_start, pri_end, pri_text in pri_entries:
        sec_text = find_overlapping_secondary(pri_start, pri_end, sec_entries)

        out_lines.append(str(srt_idx))
        out_lines.append(f"{format_time(pri_start)} --> {format_time(pri_end)}")
        out_lines.append(pri_text)
        if sec_text and sec_text != pri_text:
            out_lines.append(sec_text)
        out_lines.append('')
        srt_idx += 1

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_lines))

    print(f"Output:    {srt_idx - 1} segments -> {out_file}", file=sys.stderr)


if __name__ == '__main__':
    main()

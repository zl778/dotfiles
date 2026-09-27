#!/usr/bin/env python3
"""
Align English and Chinese SRT subtitles into a clean sentence-by-sentence
bilingual text file (no timestamps, no SRT numbering).

Merges both languages into complete sentences, splits into individual
sentences by punctuation, then aligns by time overlap to produce
one-to-one EN/ZH pairs suitable for reading or study.

Usage:
    python3 align_bilingual_sentences.py <en.srt> <zh.srt> <output.txt>

Example:
    python3 align_bilingual_sentences.py video.en.srt video.zh-Hans.srt video.bilingual.txt
"""

import re
import sys


def parse_srt(filepath):
    """Parse an SRT file into a list of (idx, start_sec, end_sec, text)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.split(r'\n\n+', content.strip())
    entries = []

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue
        try:
            idx = int(lines[0].strip())
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
        text = ' '.join(lines[2:]).strip()
        entries.append((idx, start, end, text))

    return entries


def merge_continuous_text(entries):
    """Merge consecutive SRT entries into complete sentences.

    Merges if the gap is < 0.5s AND the previous segment does NOT end
    with sentence-ending punctuation (. ! ? and Chinese equivalents).
    """
    merged = []
    current_text = ""
    current_start = None
    current_end = None

    for idx, start, end, text in entries:
        if not current_text:
            current_text = text
            current_start = start
            current_end = end
        else:
            gap = start - current_end
            ends_with_punct = (
                current_text.rstrip()[-1] in '.!?\u3002\uff01\uff1f'
                if current_text.rstrip() else False
            )

            if gap < 0.5 and not ends_with_punct:
                if current_text.endswith('-'):
                    current_text = current_text[:-1] + text
                else:
                    current_text += ' ' + text
                current_end = end
            else:
                merged.append((current_text, current_start, current_end))
                current_text = text
                current_start = start
                current_end = end

    if current_text:
        merged.append((current_text, current_start, current_end))

    return merged


def split_english_sentences(text):
    """Split English text into individual sentences on . ! ?"""
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]


def split_chinese_sentences(text):
    """Split Chinese text into individual sentences on 。！？"""
    return [s.strip() for s in re.split(r'(?<=[\u3002\uff01\uff1f])\s*', text) if s.strip()]


def distribute_time_across_sentences(sentences, start, end):
    """Distribute a single segment's time range evenly across sentences."""
    if not sentences:
        return []
    if len(sentences) == 1:
        return [(sentences[0], start, end)]
    seg_duration = (end - start) / len(sentences)
    result = []
    for i, s in enumerate(sentences):
        s_start = start + i * seg_duration
        s_end = s_start + seg_duration
        result.append((s, s_start, s_end))
    return result


def align_by_time(en_entries, zh_entries):
    """Align individual English sentences to Chinese sentences by time overlap."""
    # Split both into individual sentences with distributed time ranges
    en_sentences = []
    for text, start, end in en_entries:
        sents = split_english_sentences(text)
        en_sentences.extend(distribute_time_across_sentences(sents, start, end))

    zh_sentences = []
    for text, start, end in zh_entries:
        sents = split_chinese_sentences(text)
        zh_sentences.extend(distribute_time_across_sentences(sents, start, end))

    print(f"EN individual sentences: {len(en_sentences)}", file=sys.stderr)
    print(f"ZH individual sentences: {len(zh_sentences)}", file=sys.stderr)

    # Align: for each English sentence, find the Chinese sentence with the
    # most time overlap
    aligned = []
    for en_text, en_start, en_end in en_sentences:
        best_zh = ""
        best_overlap = 0
        for zh_text, zh_start, zh_end in zh_sentences:
            overlap = max(0, min(en_end, zh_end) - max(en_start, zh_start))
            if overlap > best_overlap:
                best_overlap = overlap
                best_zh = zh_text

        aligned.append((en_text, best_zh))

    return aligned


def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <en.srt> <zh.srt> <output.txt>", file=sys.stderr)
        sys.exit(1)

    en_file, zh_file, out_file = sys.argv[1], sys.argv[2], sys.argv[3]

    en_raw = parse_srt(en_file)
    zh_raw = parse_srt(zh_file)

    en_merged = merge_continuous_text(en_raw)
    zh_merged = merge_continuous_text(zh_raw)

    print(f"EN raw: {len(en_raw)} -> merged: {len(en_merged)}", file=sys.stderr)
    print(f"ZH raw: {len(zh_raw)} -> merged: {len(zh_merged)}", file=sys.stderr)

    aligned = align_by_time(en_merged, zh_merged)

    lines = []
    for en, zh in aligned:
        lines.append(en)
        if zh:
            lines.append(zh.strip())
        lines.append("")

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    with_zh = sum(1 for _, zh in aligned if zh)
    print(f"Total pairs: {len(aligned)}, with ZH: {with_zh}", file=sys.stderr)
    print(f"Output: {out_file}", file=sys.stderr)


if __name__ == '__main__':
    main()

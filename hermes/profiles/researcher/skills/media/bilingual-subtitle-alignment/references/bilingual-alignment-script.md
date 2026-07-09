# Bilingual SRT Alignment Script

Full working Python script for aligning two SRT subtitle files by time overlap, producing sentence-by-sentence bilingual output.

## Usage

```bash
python3 align_bilingual_srt.py en.srt zh-Hans.srt output.txt
```

## Script

```python
#!/usr/bin/env python3
"""
Align bilingual SRT files by time overlap at the sentence level.

Usage:
    python3 align_bilingual_srt.py <lang1.srt> <lang2.srt> <output.txt>
"""
import re
import sys


def parse_srt(filepath):
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
            return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000.0

        start = to_sec(*[int(g) for g in time_match.groups()[:4]])
        end = to_sec(*[int(g) for g in time_match.groups()[4:]])
        text = ' '.join(lines[2:]).strip()
        entries.append((idx, start, end, text))
    return entries


def merge_continuous_text(entries):
    """Merge consecutive SRT entries into complete sentences.
    
    Rule: if gap < 0.5s AND previous segment doesn't end with
    sentence-ending punctuation, merge them.
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


def split_sentences(text):
    """Split text into individual sentences by punctuation."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    result = []
    for s in sentences:
        s = s.strip()
        if s:
            result.append(s)
    return result


def split_chinese_sentences(text):
    """Split Chinese text into individual sentences."""
    sentences = re.split(r'(?<=[\u3002\uff01\uff1f])\s*', text)
    result = []
    for s in sentences:
        s = s.strip()
        if s:
            result.append(s)
    return result


def align_by_time(en_sentences, zh_individual):
    """Align each English sentence to best Chinese match by time overlap."""
    aligned = []
    for en_text, en_start, en_end in en_sentences:
        best_zh = ""
        best_overlap = 0
        for zh_text, zh_start, zh_end in zh_individual:
            overlap = max(0, min(en_end, zh_end) - max(en_start, zh_start))
            if overlap > best_overlap:
                best_overlap = overlap
                best_zh = zh_text
        aligned.append((en_text, best_zh))
    return aligned


def main():
    en_file = sys.argv[1]
    zh_file = sys.argv[2]
    output_file = sys.argv[3]

    en_raw = parse_srt(en_file)
    zh_raw = parse_srt(zh_file)

    en_merged = merge_continuous_text(en_raw)
    zh_merged = merge_continuous_text(zh_raw)

    # Split into individual sentences for finer alignment
    en_sentences = []
    for text, start, end in en_merged:
        sents = split_sentences(text)
        if not sents:
            sents = [text]
        if len(sents) == 1:
            en_sentences.append((sents[0], start, end))
        else:
            seg_dur = (end - start) / len(sents)
            for i, s in enumerate(sents):
                s_start = start + i * seg_dur
                s_end = s_start + seg_dur
                en_sentences.append((s, s_start, s_end))

    zh_individual = []
    for text, start, end in zh_merged:
        sents = split_chinese_sentences(text)
        if not sents:
            sents = [text]
        if len(sents) == 1:
            zh_individual.append((sents[0], start, end))
        else:
            seg_dur = (end - start) / len(sents)
            for i, s in enumerate(sents):
                s_start = start + i * seg_dur
                s_end = s_start + seg_dur
                zh_individual.append((s, s_start, s_end))

    aligned = align_by_time(en_sentences, zh_individual)

    lines = []
    for en, zh in aligned:
        lines.append(en)
        if zh:
            lines.append(zh.strip())
        lines.append("")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    with_zh = sum(1 for _, zh in aligned if zh)
    print(f"Total: {len(aligned)} pairs, with translation: {with_zh}")


if __name__ == '__main__':
    main()
```

## When This Script Is Needed

- `youtube-transcript-api` is IP-blocked by YouTube (common from cloud/office IPs)
- The user wants bilingual subtitles, not just a single-language transcript
- YouTube auto-translate subtitles exist but need alignment with the original
- The user specifically asks for "一句对一句" (sentence-by-sentence) format without timestamps

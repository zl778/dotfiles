---
name: bilingual-subtitle-alignment
description: "Align bilingual subtitles (e.g. English + Chinese) from SRT files into sentence-by-sentence parallel text. Parses, merges broken segments, and aligns by time overlap."
platforms: [linux, macos, windows]
---

# Bilingual Subtitle Alignment

Align subtitles in two languages from SRT files into clean sentence-by-sentence parallel text. Supports YouTube auto-translated subtitles, manually uploaded subtitles, or any SRT source where the two languages share a common timeline.

## When to Use

- User has a video with subtitles in two languages (e.g. English + Chinese) and wants a sentence-by-sentence bilingual transcript
- YouTube auto-translate subtitles (zh-Hans from en) need alignment because the segmentation differs from the original
- Any SRT files from different languages that share the same video timeline

## Workflow

### 1. Download Subtitles

For YouTube videos, use yt-dlp with browser cookies:

```bash
# List available subtitles
yt-dlp --cookies-from-browser chrome --list-subs <URL>

# Download a specific language subtitle
yt-dlp --cookies-from-browser chrome --write-subs --sub-langs "en" --sub-format srt --skip-download -o "%(id)s" <URL>

# Download auto-translated subtitles (e.g. Chinese from English)
yt-dlp --cookies-from-browser chrome --write-auto-subs --sub-langs "zh-Hans" --sub-format srt --skip-download -o "%(id)s" <URL>
```

**Important:** `--write-subs` for original subtitles, `--write-auto-subs` for YouTube's auto-translated subtitles. They are separate flags.

### 2. Align by Time Overlap

The core technique: parse both SRTs, merge broken sentence segments, split into individual sentences, then align by time overlap.

**Python approach:**

```python
import re

def parse_srt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    blocks = re.split(r'\n\n+', content.strip())
    entries = []
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3: continue
        try: idx = int(lines[0].strip())
        except ValueError: continue
        time_match = re.match(
            r'(\d{1,2}:\d{2}:\d{2})[,.]\d{3}\s*-->\s*(\d{1,2}:\d{2}:\d{2})[,.]\d{3}',
            lines[1]
        )
        if not time_match: continue
        def to_sec(h, m, s, ms): return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000.0
        # parse h,m,s,ms from time_match groups... (simplified)
        start, end = (...compute...)
        text = ' '.join(lines[2:]).strip()
        entries.append((idx, start, end, text))
    return entries
```

**Key Algorithm — Sentence-level alignment:**

1. **Merge** consecutive SRT entries into complete sentences:
   - If gap < 0.5s AND previous segment doesn't end with sentence-ending punctuation (.!?。！？) → merge
   - Otherwise → start a new sentence
2. **Split** each merged entry into individual sentences by punctuation
3. **Align** each English sentence to the Chinese sentence with the most time overlap

**See the full working script** at `references/bilingual-alignment-script.md`.

### 3. Output Formats

- **SRT bilingual format**: English line followed by Chinese line per subtitle entry
- **Plain text format**: English sentence, blank line, Chinese sentence, blank line
- **With or without timestamps** depending on user preference

## Pitfalls

### YouTube Auto-Translate Segmentation Mismatch

YouTube's auto-translated subtitles (zh-Hans) often have **different segmentation** from the original English. One Chinese segment may span 3-4 English segments. Time-overlap alignment handles this, but some early/late pairs may still be slightly off.

- **Symptom**: First few pairs show the same Chinese text repeated across multiple English sentences
- **Fix**: The time-overlap algorithm naturally corrects this after 5-10 segments as the timelines converge

### cp -R on macOS

When copying .app bundles: `cp -R` on an existing directory **merges** rather than replaces. Always `rm -rf` the target first.

### yt-dlp Cookies

YouTube blocks requests from cloud IPs. Always use `--cookies-from-browser chrome` (or your browser) for reliable subtitle downloads on YouTube.

## Verification

```bash
# Check alignment quality manually
head -20 <output_file>

# Count pairs
grep -c "^[A-Z]" <output_file>   # approximate English sentence count
grep -c "^$" <output_file>        # blank line separator count
```

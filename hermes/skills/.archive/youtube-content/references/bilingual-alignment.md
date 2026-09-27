# Bilingual Subtitle Processing

## Overview

Two complementary scripts for handling bilingual subtitles from YouTube:

| Script | Input | Output | Use Case |
|--------|-------|--------|----------|
| `merge_bilingual_subs.py` | 2 SRT files | 1 bilingual SRT | Import into video player (VLC, IINA, etc.) — keeps timestamps |
| `align_bilingual_sentences.py` | 2 SRT files | 1 plain-text file | Reading / study — no timestamps, sentences merged into clean EN/ZH pairs |

## When to use which

- **merge_bilingual_subs.py**: The user says "生成中英文字幕文件" or "双语字幕" — they want a playable SRT. Uses the primary language's timeline as the anchor; secondary text is looked up by timestamp overlap. The output preserves SRT timestamps and numbering so any media player can display both languages simultaneously.

- **align_bilingual_sentences.py**: The user says "一句对一句的中文翻译" or "不需要时间" — they want a clean text file for reading/study. This script merges broken segments into complete sentences, splits both languages into individual sentences by punctuation, then aligns by time overlap. The output is a plain text file with EN/ZH pairs separated by blank lines, no timestamps.

## Alignment accuracy notes

- Both scripts work best when the two SRT files cover the same video (same audio).
- YouTube's auto-translated subtitles (`zh-Hans`, `ja`, etc.) often have different segmentation than the original English — the sentence-level aligner handles this better by splitting both into individual sentences first.
- A few pairs may still misalign (e.g., a short English fragment matched to a previous Chinese sentence). This is inherent when the source languages have different segmentation granularity.
- For perfect translation quality, use the auto-captions from YouTube as a starting point, then manually review or use an LLM pass on the output.

## Workflow with yt-dlp

```bash
# 1. List available subtitles
yt-dlp --cookies-from-browser chrome --list-subs "VIDEO_URL"

# 2. Download both languages (example: English + Simplified Chinese)
yt-dlp --cookies-from-browser chrome --write-subs --write-auto-subs \
  --sub-langs "en,zh-Hans" --sub-format srt --skip-download -o "%(id)s" "VIDEO_URL"

# 3. Merge into bilingual SRT (playable)
python3 ../scripts/merge_bilingual_subs.py \
  video_id.en.srt video_id.zh-Hans.srt video_id.bilingual.srt

# 4. Or align into sentence-by-sentence text (readable)
python3 ../scripts/align_bilingual_sentences.py \
  video_id.en.srt video_id.zh-Hans.srt video_id.transcript.txt
```

## Known quirks

- YouTube's auto-translate for `zh-Hans` uses `zh-Hans-en` as the track name in `--list-subs`.
- `--write-subs` downloads human-created captions; `--write-auto-subs` downloads machine-generated ones.
- Some videos only have auto-captions (no manual subtitles). Always use `--write-auto-subs` unless `--list-subs` shows a non-automatic entry.
- Chinese punctuation spaces: YouTube's auto-translated Chinese often has extra spaces around Chinese text (e.g., "学习薄 挤出" instead of "学习薄挤出"). These are an artifact of the translation pipeline. The alignment scripts don't clean them — that's a post-processing concern if the user wants it.

---
name: youtube-content
description: "YouTube transcripts to summaries, threads, blogs."
platforms: [linux, macos, windows]
---

# YouTube Content Tool

## When to use

Use when the user shares a YouTube URL or video link, asks to summarize a video, requests a transcript, or wants to extract and reformat content from any YouTube video. Transforms transcripts into structured content (chapters, summaries, threads, blog posts).

Extract transcripts from YouTube videos and convert them into useful formats.

## Setup

```bash
pip install youtube-transcript-api
```

## Helper Scripts

`SKILL_DIR` is the directory containing this SKILL.md file.

### fetch_transcript.py

Accepts any standard YouTube URL format, short links (youtu.be), shorts, embeds, live links, or a raw 11-character video ID.

```bash
# JSON output with metadata
python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text (good for piping into further processing)
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only

# With timestamps
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# Specific language with fallback chain
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
```

### merge_bilingual_subs.py

Merge two SRT files into a single bilingual SRT (playable in VLC, IINA, etc.). Primary language's timeline is used as the anchor.

```bash
python3 SKILL_DIR/scripts/merge_bilingual_subs.py primary.srt secondary.srt output.srt
```

### align_bilingual_sentences.py

Align two SRT files into a clean sentence-by-sentence bilingual text file (no timestamps). Merges broken segments into full sentences before aligning by time overlap.

```bash
python3 SKILL_DIR/scripts/align_bilingual_sentences.py en.srt zh.srt output.txt
```

## Output Formats

After fetching the transcript, format it based on what the user asks for:

- **Chapters**: Group by topic shifts, output timestamped chapter list
- **Summary**: Concise 5-10 sentence overview of the entire video
- **Chapter summaries**: Chapters with a short paragraph summary for each
- **Thread**: Twitter/X thread format — numbered posts, each under 280 chars
- **Blog post**: Full article with title, sections, and key takeaways
- **Quotes**: Notable quotes with timestamps

### Example — Chapters Output

```
00:00 Introduction — host opens with the problem statement
03:45 Background — prior work and why existing solutions fall short
12:20 Core method — walkthrough of the proposed approach
24:10 Results — benchmark comparisons and key takeaways
31:55 Q&A — audience questions on scalability and next steps
```

## Workflow

1. **Fetch** the transcript using the helper script with `--text-only --timestamps`.
2. **Validate**: confirm the output is non-empty and in the expected language. If empty, retry without `--language` to get any available transcript.
3. **Fallback if API blocked** — If `youtube-transcript-api` is IP-blocked, do NOT jump straight to audio transcription. First check for downloadable subtitles:
   ```bash
   yt-dlp --cookies-from-browser chrome --list-subs "URL"
   ```
   If subtitles exist, download them with `--write-subs --write-auto-subs --sub-langs ...`. This is faster, cheaper, and higher quality than transcribing audio. See **Error Handling** below for full commands.
4. **Chunk if needed**: if the transcript exceeds ~50K characters, split into overlapping chunks (~40K with 2K overlap) and summarize each chunk before merging.
5. **Transform** into the requested output format. If the user did not specify a format, default to a summary.
6. **Verify**: re-read the transformed output to check for coherence, correct timestamps, and completeness before presenting.

## Error Handling

- **Transcript disabled**: tell the user; suggest they check if subtitles are available on the video page.
- **Private/unavailable video**: relay the error and ask the user to verify the URL.
- **No matching language**: retry without `--language` to fetch any available transcript, then note the actual language to the user.
- **Dependency missing**: run `pip install youtube-transcript-api` and retry.
- **YouTube blocks transcript API / IP blocked**: if `youtube-transcript-api` reports IP blocking or `yt-dlp` says `Sign in to confirm you're not a bot`, use a multi-step fallback chain. Try these **in order** — each is cheaper than the next.

    **Step 1 — Check for existing auto-captions via yt-dlp with browser cookies.**  
    Before transcribing audio, check if YouTube already has subtitles you can download directly:

    ```bash
    # List available subtitles (both manual and auto-generated)
    yt-dlp --cookies-from-browser chrome --list-subs "VIDEO_URL"

    # Download specific languages
    yt-dlp --cookies-from-browser chrome --write-subs --write-auto-subs \
      --sub-langs "en,zh-Hans" --sub-format srt --skip-download -o "%(id)s" "VIDEO_URL"
    ```

    The `--write-auto-subs` flag fetches YouTube's auto-generated captions and machine translations. `--sub-langs` accepts any language code shown in `--list-subs` output. `--skip-download` avoids downloading the video file. This is faster and higher quality than audio transcription.

    If subtitles were downloaded and the user wants bilingual output, use the helper scripts:
    ```bash
    # Bilingual SRT (playable in video player)
    python3 SKILL_DIR/scripts/merge_bilingual_subs.py video_id.en.srt video_id.zh-Hans.srt video_id.bilingual.srt

    # Sentence-by-sentence text (reading/study, no timestamps)
    python3 SKILL_DIR/scripts/align_bilingual_sentences.py video_id.en.srt video_id.zh-Hans.srt video_id.transcript.txt
    ```

    **Step 2 — Transcribe locally with Whisper** (if no auto-captions exist or the right language is missing):

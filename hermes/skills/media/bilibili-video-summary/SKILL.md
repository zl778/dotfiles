---
name: bilibili-video-summary
description: Use when the user provides a Bilibili video URL and asks for a summary, transcript, chapters, commands, or an Obsidian note. Extract the audio, transcribe locally with mlx-whisper when possible, correct ASR errors, and deliver a verified structured summary.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [bilibili, video, audio, transcription, whisper, obsidian]
    related_skills: [youtube-content, obsidian, obsidian-note-authoring]
---

# Bilibili Video Summary

## Overview

Use a filesystem-first workflow to turn a Bilibili video into a reliable Chinese summary. Prefer subtitles when they are directly available, but fall back to extracting the audio stream and running local Whisper transcription. Treat the transcript as noisy ASR data: correct obvious product names, commands, acronyms, and proper nouns before summarizing.

The completed task should produce a real transcript and a grounded summary, not a guessed outline from the title and description.

## When to Use

- The user provides a `bilibili.com/video/BV...` URL and asks for a summary.
- The user asks to extract spoken content, chapters, commands, or key points from a Bilibili video.
- The user wants the result saved to Obsidian.

Do not claim the video was summarized until audio/subtitles were actually retrieved and the resulting transcript was read.

## Workflow

### 1. Inspect the page and identify the video

Open the URL with the browser when needed and record:

- title;
- duration;
- description;
- BVID;
- whether the page exposes subtitles.

Ignore tracking query parameters such as `spm_id_from` and `vd_source` when constructing the clean URL.

If the page itself is inaccessible, report the concrete error and ask for a subtitle file or local video file instead of inventing content.

### 2. Try the cheap extraction paths first

First try available subtitles or metadata. `yt-dlp` may work for some videos:

```bash
yt-dlp --skip-download --list-subs "VIDEO_URL"
```

If subtitles are available, download them and use them as the primary source. If `yt-dlp` fails with Bilibili HTTP 412 while requesting `x/player/wbi/playurl`, do not retry the same command repeatedly. Use the fallback in the next section.

### 3. Bilibili HTTP 412 fallback: use the legacy playurl endpoint

Fetch the Bilibili HTML and extract `aid` and `cid` from the embedded page data. The page commonly contains values like:

```text
aid: 116912482749717
cid: 39913587043
```

Then request the non-WBI endpoint:

```text
https://api.bilibili.com/x/player/playurl
```

with these parameters:

```text
avid=<aid>
cid=<cid>
qn=16
fnval=16
fnver=0
fourk=1
```

Use headers including:

```text
User-Agent: Mozilla/5.0
Referer: https://www.bilibili.com/video/<BVID>/
```

Verify that the JSON response has `code: 0` and a `data.dash.audio` array. Select an audio entry, preferring a higher bandwidth entry when practical, and download its `baseUrl` (or `base_url`) with the same User-Agent and Referer headers.

The audio stream may be an `.m4s` file even though its content type is `video/mp4`. Confirm the downloaded file is non-empty and has a plausible media duration.

### 4. Convert audio for Whisper

Use FFmpeg to create a mono 16 kHz PCM WAV:

```bash
ffmpeg -y -i INPUT.m4s -vn -ac 1 -ar 16000 -c:a pcm_s16le OUTPUT.wav
```

Verify the output with `ffprobe` or FFmpeg output. The duration should approximately match the video duration.

Use a temporary working directory such as:

```text
~/tmp-bili/<BVID>/
```

Keep the original downloaded audio and converted WAV until the transcript and summary have been verified.

### 5. Run mlx-whisper correctly on macOS Apple Silicon

Do not use:

```bash
python3.13 -m mlx_whisper
```

The package may not provide `mlx_whisper.__main__`. Use the installed console script instead, commonly:

```bash
~/Library/Python/3.13/bin/mlx_whisper \
  INPUT.wav \
  --model mlx-community/whisper-large-v3-turbo \
  --language Chinese \
  --output-format txt \
  --output-dir TRANSCRIPT_DIR
```

Check the executable first:

```bash
which mlx_whisper
ls -l ~/Library/Python/3.13/bin/mlx_whisper
```

If model download fails with:

```text
Using SOCKS proxy, but the 'socksio' package is not installed
```

install the missing dependency with the same Python environment:

```bash
python3.13 -m pip install --user socksio
```

Then rerun the console script. Do not reinstall Whisper unnecessarily when the package is already present.

Verify that the output directory contains a non-empty `.txt` file:

```bash
ls -lh TRANSCRIPT_DIR
wc -l -c TRANSCRIPT.txt
```

For long videos, keep the full transcript on disk and read it in chunks rather than truncating it silently.

### 6. Validate and clean the transcript

Before summarizing:

- confirm the transcript is non-empty;
- confirm the language is expected;
- identify obvious ASR substitutions;
- correct product names, commands, acronyms, model names, and technical terms;
- do not silently convert uncertain words into facts;
- mark uncertain corrections when they affect execution.

Typical Bilibili ASR errors include:

| ASR output | Likely correction |
|---|---|
| AA Agent / AA | AI Agent |
| Carly Linux | Kali Linux |
| Hermis Agent | Hermes Agent |
| Cloud Code | Claude Code |
| Grip | grep |
| 速度 apt | sudo apt |
| WSL-L | `wsl -l` |
| WSL-D | `wsl -d` |
| WSL-update | `wsl --update` |
| WSL-install | `wsl --install` |
| 挂载券 | 挂载卷 |
| NVIDIA-SMI | `nvidia-smi` |

Do not present a command as copy-ready if the transcript omitted arguments or the ASR is ambiguous. Cross-check current syntax against official documentation when the user intends to execute it.

### 7. Produce the summary

If the user did not specify a format, provide:

1. a one-paragraph executive summary;
2. the central thesis and reasons;
3. topic sections in the order presented;
4. actionable commands in fenced code blocks;
5. important caveats and security risks;
6. a section explaining relevance to the user's known environment;
7. ASR corrections and uncertainty notes;
8. a final conclusion.

The transcript produced by the helper command may not include timestamps. Do not fabricate exact timestamps. Use topic-based chapters or label any timing as approximate.

For technical videos, distinguish clearly between:

- what the speaker demonstrated;
- what is a general recommendation;
- what requires current-version verification;
- what is specifically relevant to the user.

### 8. Save to Obsidian when requested

Use the Obsidian skill and the resolved vault path. For this user's PKM vault, prefer the existing PARA convention:

```text
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/
```

Resource/reference notes generally belong under `30_Resources/`, with AI-related notes under `30_Resources/AI/` when appropriate.

Use frontmatter with:

```yaml
---
title: ...
aliases:
  - ...
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: reference
tags:
  - r/tools/hermes
  - r/...
source: https://www.bilibili.com/video/BV...
---
```

Include the source URL, the title, the duration if known, the summary, corrected commands, caveats, and links to related notes. Write the complete note with `write_file`, then read the beginning and end of the file to verify it exists and contains the expected frontmatter and conclusion.

## Common Pitfalls

1. **Using only the title and description**: these are not a video summary. Retrieve subtitles or audio first.
2. **Repeating yt-dlp after HTTP 412**: switch to the legacy `/x/player/playurl` endpoint after confirming the failure is at the WBI play URL request.
3. **Calling `python -m mlx_whisper`**: use the installed `mlx_whisper` console script.
4. **Using the wrong Python environment**: verify the executable and package paths before installing dependencies.
5. **Ignoring SOCKS proxy support**: install `socksio` into the same Python environment when Hugging Face model download reports that error.
6. **Treating ASR commands as authoritative**: correct obvious errors and verify incomplete commands before presenting them as executable.
7. **Fabricating timestamps**: if the transcript has no timestamps, use untimed chapters or clearly mark estimates.
8. **Deleting intermediate files too early**: preserve the audio and transcript until the summary has been checked.
9. **Writing an unverified Obsidian note**: after writing, read it back and report the absolute path.
10. **Putting secrets in notes**: never save API keys, cookies, bot tokens, or private credentials in the transcript or Obsidian summary.

## Verification Checklist

- [ ] Clean Bilibili URL and title recorded.
- [ ] Subtitles or audio actually retrieved.
- [ ] Audio file is non-empty and duration is plausible.
- [ ] WAV conversion succeeded.
- [ ] Whisper console script ran with the intended Python environment.
- [ ] Transcript file exists and is non-empty.
- [ ] Language and major ASR errors checked.
- [ ] Commands separated from commentary and corrected cautiously.
- [ ] No exact timestamps fabricated.
- [ ] Summary covers the whole transcript, not only the introduction.
- [ ] User-specific recommendations are clearly labeled.
- [ ] If saved to Obsidian, frontmatter, source URL, and final content were read back and verified.

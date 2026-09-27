---
name: video-content-extraction
description: "Extract, transcribe, and summarize online videos across YouTube, Bilibili, and similar platforms using subtitles first and local audio transcription as a verified fallback."
platforms: [macos, linux, windows]
---

# Video Content Extraction

## When to use

Load this skill when the user provides an online video URL and asks for a summary, transcript, chapters, commands, or an applicability analysis. It is intended for multi-platform video work, especially when a page extractor exposes only metadata but the video itself is playable.

## Core principle

Treat “page transcript unavailable” and “video unavailable” as different conditions. First try subtitles/captions; if they are absent or inaccessible, obtain the audio stream and transcribe it locally. Never invent a summary from the title or description when the user asked for the actual video content.

## Workflow

1. Identify the requested output: concise summary, chapter timeline, detailed notes, command list, critique, or platform-specific applicability analysis.
2. Inspect the URL directly and record title, duration, language, and any visible description/caption metadata.
3. Try an official/standard subtitle path first. Validate that the result is non-empty and in the expected language.
4. If subtitles fail, try a normal downloader once and inspect the actual error. Do not repeat an identical failing request.
5. For Bilibili, extract stable identifiers (`bvid`, `aid`, `cid`) from the page metadata. If the WBI-signed downloader route returns an access error, try the lower-level playback API described in `references/bilibili-audio-fallback.md`.
6. Download audio with browser-like User-Agent and Referer headers. Prefer the highest reasonable audio stream, not the whole video.
7. Convert audio with ffmpeg to mono 16 kHz WAV (or another format supported by the selected local transcription engine). Record the output path and verify its duration and non-zero size.
8. Run local Whisper transcription using the Python environment where the transcription package is installed. Inspect the interpreter/package location before invoking it; do not assume the system Python is the right environment.
9. Validate the transcript: non-empty, plausible duration/coverage, correct language, and no obvious repeated failure text. Preserve the audio and transcript so retries do not redownload the source.
10. Segment long transcripts before summarization. Produce the requested result from the transcript, retaining timestamps when chapters or quotes are requested.
11. Verify the final output against the transcript. Clearly distinguish facts stated in the video from the assistant’s own analysis and mark any unverified claims.

## Artifact and completion standard

A video-summary task is not complete after writing a plan or downloading a file. Completion requires real transcription and a summary grounded in that transcription. Report exact artifact paths and the stage reached if a tool or environment issue blocks completion. Never substitute a title/description-based guess for a failed transcript.

## Recommended output structure

- 结论/一句话摘要
- 内容概览
- 时间轴章节
- 关键步骤或命令
- 对用户场景的适用性
- 风险、过时信息和需要核实的内容
- 转写/音频文件路径（如用户需要）

## Pitfalls

- A webpage extractor may return title and description while still allowing direct media playback.
- HTTP 412 from a signed playback endpoint is not proof that the media is unavailable; try the platform’s lower-level playback API once.
- Do not report “Whisper completed” unless a real non-empty transcript exists.
- Do not discard downloaded audio when transcription setup fails; keep it as a reusable intermediate artifact.
- Do not encode a one-off missing-binary or Python-path failure as a permanent tool limitation; diagnose the environment and use the installed interpreter.

## Supporting references

- `references/bilibili-audio-fallback.md` — reproducible Bilibili identifier extraction, playback API request, audio download, ffmpeg conversion, and validation notes.

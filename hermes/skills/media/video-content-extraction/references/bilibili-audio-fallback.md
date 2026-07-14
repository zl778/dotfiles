# Bilibili audio fallback

Use this when the page is accessible and the video is playable, but a normal downloader fails at the signed playback metadata request (for example, HTTP 412).

## 1. Identify `aid` and `cid`

The Bilibili page HTML commonly contains a state object with fields similar to:

```text
aid: 116912482749717
bvid: BV1pYNm69EPm
cid: 39913587043
```

Do not guess these values. Extract them from the page response or browser state.

## 2. Request DASH playback metadata

The lower-level endpoint may work even when the WBI-signed route fails:

```text
GET https://api.bilibili.com/x/player/playurl
  ?avid=<aid>
  &cid=<cid>
  &qn=16
  &fnval=16
  &fnver=0
  &fourk=1
```

Use a browser-like User-Agent and a Referer pointing to the video page. Check that the JSON response has `code: 0` and `data.dash.audio`.

## 3. Download only audio

Select an entry from `data.dash.audio`, preferring a sensible bandwidth/codec. Download its `baseUrl` (or `base_url`) with the same headers. Save the stream as `.m4s` or `.m4a` and preserve it for retries.

## 4. Convert for local Whisper

```bash
ffmpeg -y -i input.m4s -vn -ac 1 -ar 16000 -c:a pcm_s16le output.wav
```

Verify the output has a plausible duration and non-zero size before transcription.

## 5. Transcription verification

Use the Python interpreter where `mlx-whisper` is installed, not necessarily `/usr/bin/python3`. Check the package location/interpreter first. Only after a non-empty transcript is produced should summarization begin.

## Observed reproduction

For `BV1pYNm69EPm`, the page exposed:

```text
aid = 116912482749717
cid = 39913587043
duration = about 31m31s
```

The lower-level endpoint returned audio successfully. The resulting artifacts were:

```text
/Users/liangzhu/tmp-bili/BV1pYNm69EPm.m4s
/Users/liangzhu/tmp-bili/BV1pYNm69EPm.wav
```

These paths are an example of the artifact naming pattern, not a requirement to hard-code a session-specific directory.

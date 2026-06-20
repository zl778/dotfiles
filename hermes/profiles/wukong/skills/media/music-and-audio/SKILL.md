---
name: music-and-audio
description: "Songwriting craft, AI music generation (Suno/HeartMuLa/AudioCraft), and audio analysis/visualization."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [music, audio, songwriting, suno, spectrogram, generation, analysis, creative]
    related_skills: [humanizer]
---

# Music and Audio

## Overview

Comprehensive music and audio skills covering the full creative pipeline: writing lyrics, generating songs with AI tools, and analyzing audio output.

## When to Use

| Mode | Trigger |
|------|---------|
| Songwriting | User asks to write lyrics, create a song, craft a Suno prompt |
| Music Generation | User wants to generate audio from text (HeartMuLa, AudioCraft, Suno) |
| Audio Analysis | User wants spectrograms, feature analysis, or audio visualization |
| Parody | User wants to adapt an existing song with new lyrics |

---

## Section A: Songwriting Craft

### Song Structure

Common skeletons — mix, modify, or throw out:

| Pattern | Structure | Genre |
|---------|-----------|-------|
| ABABCB | Verse/Chorus/Verse/Chorus/Bridge/Chorus | Most pop/rock |
| AABA | Verse/Verse/Bridge/Verse (refrain) | Jazz standards |
| ABAB | Verse/Chorus alternating | Simple, direct |
| AAA | Strophic (no chorus) | Folk, storytelling |

Building blocks: Intro → Verse → Pre-Chorus → Chorus → Bridge → Outro

### Rhyme and Meter

**Rhyme types** (mix them — all perfect sounds like a nursery rhyme):
- Perfect: lean/mean
- Family: crate/braid
- Assonance: had/glass (same vowels)
- Consonance: scene/when (similar endings)
- Near/slant: suggests connection without locking it down

**Meter**: The rhythm of stressed vs unstressed syllables. Say it out loud. If you stumble, the meter needs work.

### Emotional Arc and Dynamics

```
Intro: 2-3 | Verse: 5-6 | Pre-Chorus: 7 | Chorus: 8-9 | Bridge: varies | Final: 9-10
```

The most powerful trick: CONTRAST. Whisper before a scream. Sparse before dense. Silence is an instrument.

### Writing Lyrics That Work

- **SHOW, DON'T TELL**: "Your hoodie's still on the hook" > "I was sad"
- **The Hook**: The line people remember. Usually the title or core phrase.
- **Prosody**: Stable feelings → settled melodies, perfect rhymes. Longing → wandering melodies, near-rhymes.
- **AVOID**: Clichés on autopilot, Yoda-speak to force rhymes, flat dynamics.

### Parody and Adaptation

1. Map the original structure: syllables per line, rhyme scheme, stressed syllables
2. Match stressed syllables to the same beats
3. On held notes, match the vowel sound
4. Keep some original lines for recognizability

---

## Section B: Suno AI Prompt Engineering

### Style/Genre Description

Formula: Genre + Mood + Era + Instruments + Vocal Style + Production + Dynamics

```text
BAD: "sad rock song"
GOOD: "Cinematic orchestral spy thriller, 1960s Cold War era, smoky
       sultry female vocalist, big band jazz, brass section with
       trumpets and french horns, sweeping strings, minor key"
```

**Describe the journey**, not just the genre:
```text
"Begins as a haunting whisper over sparse piano. Gradually layers
 in muted brass. Builds through the chorus with full orchestra."
```

### Metatags (inside lyrics field)

| Category | Tags |
|----------|------|
| Structure | `[Intro]`, `[Verse]`, `[Chorus]`, `[Bridge]`, `[Outro]` |
| Vocal | `[Whispered]`, `[Belted]`, `[Falsetto]`, `[Harmonies]` |
| Dynamics | `[High Energy]`, `[Building Energy]`, `[Emotional Climax]` |
| Atmosphere | `[Melancholic]`, `[Euphoric]`, `[Nostalgic]` |

### Phonetic Tricks for AI Singers

- Spell words as they SOUND: "through" → "thru"
- ALL CAPS = louder
- Vowel extension: "lo-o-o-ove"
- Spell out numbers: "24/7" → "twenty four seven"
- Space acronyms: "AI" → "A I"

### Custom Mode

Always use Custom Mode for serious work. Lyrics field limit ~3,000 chars. Always add structural tags — without them Suno defaults to flat structure.

---

## Section C: HeartMuLa — Open-Source Music Generation

HeartMuLa is a family of open-source music foundation models (Apache-2.0) that generates music conditioned on lyrics and tags. Requires a GPU (8GB+ VRAM).

### Quick Install
```bash
git clone https://github.com/HeartMuLa/heartlib.git
cd heartlib
uv venv --python 3.10 .venv
. .venv/bin/activate
uv pip install -e .
uv pip install --upgrade datasets transformers
```

### Usage
```bash
cd heartlib && . .venv/bin/activate
python ./examples/run_music_generation.py \
  --model_path=./ckpt --version="3B" \
  --lyrics="./assets/lyrics.txt" --tags="./assets/tags.txt" \
  --save_path="./assets/output.mp3" --lazy_load true
```

### Key Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--topk` | 50 | Top-k sampling |
| `--temperature` | 1.0 | Sampling temperature |
| `--cfg_scale` | 1.5 | Classifier-free guidance |
| `--max_audio_length_ms` | 240000 | 4 minutes max |

See `references/music-generation-heartmula.md` for full installation, dependency patches (required for transformers 5.x), hardware requirements, and troubleshooting.

---

## Section D: songsee — Audio Spectrograms & Analysis

Generate spectrograms and multi-panel audio feature visualizations.

### Quick Start
```bash
songsee track.mp3 -o spectrogram.png
songsee track.mp3 --viz spectrogram,mel,chroma,hpss,mfcc
```

### Visualization Types
| Type | Description |
|------|-------------|
| `spectrogram` | Standard frequency spectrogram |
| `mel` | Mel-scaled spectrogram |
| `chroma` | Pitch class distribution |
| `hpss` | Harmonic/percussive separation |
| `mfcc` | Mel-frequency cepstral coefficients |

### Common Flags
| Flag | Description |
|------|-------------|
| `--style` | Color: classic, magma, inferno, viridis |
| `--start`/`--duration` | Time slice |
| `--format` | jpg or png |
| `-o` | Output file path |

Output images can be inspected with `vision_analyze` for automated audio analysis.

---

## References

| File | Description |
|------|-------------|
| `references/music-generation-heartmula.md` | Full HeartMuLa install, patches, troubleshooting |
| `references/music-generation-audiocraft.md` | AudioCraft/MusicGen text-to-music and AudioGen text-to-sound |

## Common Pitfalls

1. **Don't use bf16 for HeartCodec** — degrades audio quality. Use fp32.
2. **Tags may be ignored by HeartMuLa** — lyrics tend to dominate; experiment with tag ordering.
3. **Suno style can drift in extensions** — restate genre/mood when extending.
4. **Phonetic tricks are baked in** — fix pronunciation in lyrics BEFORE generating.
5. **Don't use artist names in Suno prompts** — describe the sound instead.
6. **HeartMuLa requires Python 3.10** — won't work with newer versions without patches.

## Verification Checklist

- [ ] Song has clear structure (verse/chorus/bridge)
- [ ] Lyrics use varied rhyme types (not all perfect)
- [ ] Emotional arc mapped (contrast, dynamics)
- [ ] Suno style describes the journey, not just genre
- [ ] Suno metatags added for performance direction
- [ ] HeartMuLa: VRAM checked before generation
- [ ] Audio output saved to expected path

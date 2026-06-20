# HeartMuLa — Music Generation Reference

## Overview
HeartMuLa is an open-source family of music foundation models (Apache-2.0) that generates music from lyrics + tags. Includes HeartCodec (12.5Hz music codec), HeartTranscriptor (lyrics transcription), and HeartCLAP (audio-text alignment).

## Hardware Requirements
- **Minimum**: 8GB VRAM with `--lazy_load true`
- **Recommended**: 16GB+ VRAM
- **Multi-GPU**: `--mula_device cuda:0 --codec_device cuda:1`
- 3B model with lazy_load peaks at ~6.2GB VRAM

## Full Installation

```bash
cd ~/
git clone https://github.com/HeartMuLa/heartlib.git
cd heartlib
uv venv --python 3.10 .venv
. .venv/bin/activate
uv pip install -e .
uv pip install --upgrade datasets transformers
```

## Required Patches (for transformers 5.x)

### Patch 1 — RoPE cache fix
In `src/heartlib/heartmula/modeling_heartmula.py`, inside `setup_caches`:
```python
# After reset_caches try/except, before `with device:`
from torchtune.models.llama3_1._position_embeddings import Llama3ScaledRoPE
for module in self.modules():
    if isinstance(module, Llama3ScaledRoPE) and not module.is_cache_built:
        module.rope_init()
        module.to(device)
```

### Patch 2 — HeartCodec loading fix
In `src/heartlib/pipelines/music_generation.py`:
Add `ignore_mismatched_sizes=True` to ALL `HeartCodec.from_pretrained()` calls (eager load in `__init__` and lazy load in the `codec` property).

## Model Checkpoints

```bash
hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'
hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B-happy-new-year'
hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss-20260123'
```

All 3 can be downloaded in parallel. Total: several GB.

## Full Usage

```bash
cd heartlib
. .venv/bin/activate
python ./examples/run_music_generation.py \
  --model_path=./ckpt --version="3B" \
  --lyrics="./assets/lyrics.txt" \
  --tags="./assets/tags.txt" \
  --save_path="./assets/output.mp3" \
  --lazy_load true
```

### Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--max_audio_length_ms` | 240000 | Max length (4 min) |
| `--topk` | 50 | Top-k sampling |
| `--temperature` | 1.0 | Sampling temperature |
| `--cfg_scale` | 1.5 | Classifier-free guidance |
| `--lazy_load` | false | Load/unload on demand |
| `--mula_dtype` | bfloat16 | MuLa dtype |
| `--codec_dtype` | float32 | Codec dtype (use fp32!) |

### Input Formatting

**Tags** (comma-separated, no spaces):
```
piano,happy,wedding,synthesizer,romantic
```

**Lyrics** (use bracketed structural tags):
```
[Intro]
[Verse]
Your lyrics here...
[Chorus]
Chorus lyrics...
```

## Performance
- RTF ≈ 1.0 (4-minute song → ~4 minutes to generate)
- Output: MP3, 48kHz stereo, 128kbps
- Uses CUDA by default

## Pitfalls
1. **Do NOT use bf16 for HeartCodec** — degrades audio quality. Use fp32.
2. **Tags may be ignored** — known issue. Lyrics dominate; experiment with tag ordering.
3. **Triton not available on macOS** — Linux/CUDA only for GPU acceleration.
4. **RTX 5080 incompatibility** reported upstream.
5. **Python 3.10 required** — dependency pin conflicts.

## Links
- Repo: https://github.com/HeartMuLa/heartlib
- Models: https://huggingface.co/HeartMuLa
- Paper: https://arxiv.org/abs/2601.10547
- License: Apache-2.0

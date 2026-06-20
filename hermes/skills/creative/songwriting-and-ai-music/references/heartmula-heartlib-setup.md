1|---
2|name: heartmula
3|description: "HeartMuLa: Suno-like song generation from lyrics + tags."
4|version: 1.0.0
5|platforms: [linux, macos, windows]
6|metadata:
7|  hermes:
8|    tags: [music, audio, generation, ai, heartmula, heartcodec, lyrics, songs]
9|    related_skills: [audiocraft]
10|---
11|
12|# HeartMuLa - Open-Source Music Generation
13|
14|## Overview
15|HeartMuLa is a family of open-source music foundation models (Apache-2.0) that generates music conditioned on lyrics and tags, with multilingual support. Generates full songs from lyrics + tags. Comparable to Suno for open-source. Includes:
16|- **HeartMuLa** - Music language model (3B/7B) for generation from lyrics + tags
17|- **HeartCodec** - 12.5Hz music codec for high-fidelity audio reconstruction
18|- **HeartTranscriptor** - Whisper-based lyrics transcription
19|- **HeartCLAP** - Audio-text alignment model
20|
21|## When to Use
22|- User wants to generate music/songs from text descriptions
23|- User wants an open-source Suno alternative
24|- User wants local/offline music generation
25|- User asks about HeartMuLa, heartlib, or AI music generation
26|
27|## Hardware Requirements
28|- **Minimum**: 8GB VRAM with `--lazy_load true` (loads/unloads models sequentially)
29|- **Recommended**: 16GB+ VRAM for comfortable single-GPU usage
30|- **Multi-GPU**: Use `--mula_device cuda:0 --codec_device cuda:1` to split across GPUs
31|- 3B model with lazy_load peaks at ~6.2GB VRAM
32|
33|## Installation Steps
34|
35|### 1. Clone Repository
36|```bash
37|cd ~/  # or desired directory
38|git clone https://github.com/HeartMuLa/heartlib.git
39|cd heartlib
40|```
41|
42|### 2. Create Virtual Environment (Python 3.10 required)
43|```bash
44|uv venv --python 3.10 .venv
45|. .venv/bin/activate
46|uv pip install -e .
47|```
48|
49|### 3. Fix Dependency Compatibility Issues
50|
51|**IMPORTANT**: As of Feb 2026, the pinned dependencies have conflicts with newer packages. Apply these fixes:
52|
53|```bash
54|# Upgrade datasets (old version incompatible with current pyarrow)
55|uv pip install --upgrade datasets
56|
57|# Upgrade transformers (needed for huggingface-hub 1.x compatibility)
58|uv pip install --upgrade transformers
59|```
60|
61|### 4. Patch Source Code (Required for transformers 5.x)
62|
63|**Patch 1 - RoPE cache fix** in `src/heartlib/heartmula/modeling_heartmula.py`:
64|
65|In the `setup_caches` method of the `HeartMuLa` class, add RoPE reinitialization after the `reset_caches` try/except block and before the `with device:` block:
66|
67|```python
68|# Re-initialize RoPE caches that were skipped during meta-device loading
69|from torchtune.models.llama3_1._position_embeddings import Llama3ScaledRoPE
70|for module in self.modules():
71|    if isinstance(module, Llama3ScaledRoPE) and not module.is_cache_built:
72|        module.rope_init()
73|        module.to(device)
74|```
75|
76|**Why**: `from_pretrained` creates model on meta device first; `Llama3ScaledRoPE.rope_init()` skips cache building on meta tensors, then never rebuilds after weights are loaded to real device.
77|
78|**Patch 2 - HeartCodec loading fix** in `src/heartlib/pipelines/music_generation.py`:
79|
80|Add `ignore_mismatched_sizes=True` to ALL `HeartCodec.from_pretrained()` calls (there are 2: the eager load in `__init__` and the lazy load in the `codec` property).
81|
82|**Why**: VQ codebook `initted` buffers have shape `[1]` in checkpoint vs `[]` in model. Same data, just scalar vs 0-d tensor. Safe to ignore.
83|
84|### 5. Download Model Checkpoints
85|```bash
86|cd heartlib  # project root
87|hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'
88|hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B-happy-new-year'
89|hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss-20260123'
90|```
91|
92|All 3 can be downloaded in parallel. Total size is several GB.
93|
94|## GPU / CUDA
95|
96|HeartMuLa uses CUDA by default (`--mula_device cuda --codec_device cuda`). No extra setup needed if the user has an NVIDIA GPU with PyTorch CUDA support installed.
97|
98|- The installed `torch==2.4.1` includes CUDA 12.1 support out of the box
99|- `torchtune` may report version `0.4.0+cpu` — this is just package metadata, it still uses CUDA via PyTorch
100|- To verify GPU is being used, look for "CUDA memory" lines in the output (e.g. "CUDA memory before unloading: 6.20 GB")
101|- **No GPU?** You can run on CPU with `--mula_device cpu --codec_device cpu`, but expect generation to be **extremely slow** (potentially 30-60+ minutes for a single song vs ~4 minutes on GPU). CPU mode also requires significant RAM (~12GB+ free). If the user has no NVIDIA GPU, recommend using a cloud GPU service (Google Colab free tier with T4, Lambda Labs, etc.) or the online demo at https://heartmula.github.io/ instead.
102|
103|## Usage
104|
105|### Basic Generation
106|```bash
107|cd heartlib
108|. .venv/bin/activate
109|python ./examples/run_music_generation.py \
110|  --model_path=./ckpt \
111|  --version="3B" \
112|  --lyrics="./assets/lyrics.txt" \
113|  --tags="./assets/tags.txt" \
114|  --save_path="./assets/output.mp3" \
115|  --lazy_load true
116|```
117|
118|### Input Formatting
119|
120|**Tags** (comma-separated, no spaces):
121|```
122|piano,happy,wedding,synthesizer,romantic
123|```
124|or
125|```
126|rock,energetic,guitar,drums,male-vocal
127|```
128|
129|**Lyrics** (use bracketed structural tags):
130|```
131|[Intro]
132|
133|[Verse]
134|Your lyrics here...
135|
136|[Chorus]
137|Chorus lyrics...
138|
139|[Bridge]
140|Bridge lyrics...
141|
142|[Outro]
143|```
144|
145|### Key Parameters
146|| Parameter | Default | Description |
147||-----------|---------|-------------|
148|| `--max_audio_length_ms` | 240000 | Max length in ms (240s = 4 min) |
149|| `--topk` | 50 | Top-k sampling |
150|| `--temperature` | 1.0 | Sampling temperature |
151|| `--cfg_scale` | 1.5 | Classifier-free guidance scale |
152|| `--lazy_load` | false | Load/unload models on demand (saves VRAM) |
153|| `--mula_dtype` | bfloat16 | Dtype for HeartMuLa (bf16 recommended) |
154|| `--codec_dtype` | float32 | Dtype for HeartCodec (fp32 recommended for quality) |
155|
156|### Performance
157|- RTF (Real-Time Factor) ≈ 1.0 — a 4-minute song takes ~4 minutes to generate
158|- Output: MP3, 48kHz stereo, 128kbps
159|
160|## Pitfalls
161|1. **Do NOT use bf16 for HeartCodec** — degrades audio quality. Use fp32 (default).
162|2. **Tags may be ignored** — known issue (#90). Lyrics tend to dominate; experiment with tag ordering.
163|3. **Triton not available on macOS** — Linux/CUDA only for GPU acceleration.
164|4. **RTX 5080 incompatibility** reported in upstream issues.
165|5. The dependency pin conflicts require the manual upgrades and patches described above.
166|
167|## Links
168|- Repo: https://github.com/HeartMuLa/heartlib
169|- Models: https://huggingface.co/HeartMuLa
170|- Paper: https://arxiv.org/abs/2601.10547
171|- License: Apache-2.0
172|
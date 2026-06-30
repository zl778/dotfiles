# Memory Provider Comparison

Full comparison of Hermes Agent memory options, researched and verified June 2026.

## Provider Details

### Built-in SQLite (current default)

- **GitHub**: (Hermes core, no separate repo)
- **Deployment**: Zero — file-based, uses `~/.hermes/memories/MEMORY.md` and `USER.md`
- **Dependencies**: None
- **Memory format**: Plain-text entries, manually managed by the agent
- **Storage structure**: Flat key-value pairs (entries separated by `§`)
- **Retrieval**: Full content injected into system prompt at session start
- **Temporal awareness**: None
- **Reflection/learning**: None — purely manual curation
- **Benchmarks**: N/A (not a retrieval system)
- **Offline**: ✅ Fully offline
- **Maintenance**: Agent self-manages via `memory` tool
- **Best for**: Simple needs, offline use, users who don't want extra infrastructure

### Honcho

- **GitHub**: Originally grilllab/honcho (repo now 404 — may be deprecated or renamed)
- **Deployment**: Hermes plugin + PostgreSQL database server
- **Dependencies**: PostgreSQL, Hermes honcho plugin
- **Memory format**: Automatically extracted from conversation
- **Storage structure**: User / Session / Agent three-layer hierarchy
- **Retrieval**: API-based queries
- **Temporal awareness**: Yes
- **Reflection/learning**: Limited
- **Benchmarks**: Public data scarce
- **Offline**: ❌ Requires database server
- **Maintenance**: DB admin, plugin config
- **Best for**: Multi-user isolation scenarios
- **Setup**: `hermes honcho setup` (plugin must be installed first)

### Mem0 (mem0ai/mem0)

- **GitHub**: https://github.com/mem0ai/mem0 — 59.7k stars, YC S24
- **Deployment**: `pip install mem0ai` or `npm install mem0ai` + API key (free tier available) OR self-hosted
- **Dependencies**: Mem0 API key or self-hosted instance
- **Memory format**: Automatically extracted, single-pass ADD-only (no overwrites)
- **Storage structure**: Entity-linked, semantic + BM25 keyword + entity matching
- **Retrieval**: Multi-signal (semantic, BM25, entity) scored in parallel and fused
- **Temporal awareness**: ✅ Temporal reasoning — ranks the right dated instance for queries about current state, past events, and upcoming plans
- **Reflection/learning**: Agent-generated facts are first-class citizens
- **Benchmarks** (April 2026 new algorithm):
  - LongMemEval: **94.8** (+27 pts over previous)
  - LoCoMo: **91.6** (+20 pts)
  - BEAM (1M): **64.1** (production-scale)
  - Tokens per query: ~6.8K, Latency p50: ~1s
- **Offline**: ❌ Requires API or self-hosted
- **Maintenance**: Very low — `hermes memory setup` configures automatically
- **Best for**: Easy setup (one command), strong retrieval, users wanting "set and forget" memory
- **Setup**: `hermes memory setup` → select mem0 → configure API key

### Hindsight (vectorize-io/hindsight)

- **GitHub**: https://github.com/vectorize-io/hindsight — 17.8k stars, MIT
- **Paper**: https://arxiv.org/abs/2512.12818
- **Deployment**: Docker (`docker run ghcr.io/vectorize-io/hindsight:latest`) OR embedded Python (`pip install hindsight-all`)
- **Dependencies**: Docker + OpenAI API key (or Anthropic/Gemini/Groq/Ollama/LMStudio etc.)
- **Memory format**: Automatically extracted into biomimetic structures
- **Storage structure**: Three pathways:
  - **World**: Facts about the world ("The stove gets hot")
  - **Experiences**: Agent's own experiences ("I touched the stove and it hurt")
  - **Mental Models**: Learned understanding formed by reflecting on raw memories
- **Retrieval**: Three operations:
  - `retain` — store information
  - `recall` — search memories
  - `reflect` — generate disposition-aware response using both memory + LLM reasoning
- **Temporal awareness**: ✅ Time-series representation in memory structure
- **Reflection/learning**: ✅ Yes — Mental Models update over time
- **Benchmarks**:
  - LongMemEval: **State-of-the-art** (independently reproduced by Virginia Tech + Washington Post)
  - Other scores are self-reported by vendors
- **Offline**: ❌ Requires Docker + API key (embedded mode reduces but doesn't eliminate dependency)
- **Maintenance**: Docker container lifecycle, API key management
- **Best for**: Maximum accuracy, learning-capable agents, production enterprise use (Fortune 500)
- **Integration**: Hermes has built-in plugin (`memory.provider: hindsight`)

## Quick Decision Matrix

| Your priority | Pick | Why |
|--------------|------|-----|
| **Zero infra, offline** | Built-in SQLite | No dependencies, works offline, just cleaned up ✅ |
| **One command, auto-magic** | Mem0 | `hermes memory setup` → done. Strong benchmarks. |
| **Maximum accuracy** | Hindsight | SOTA benchmarks, independently verified, Fortune 500 production |
| **Multi-user isolation** | Honcho | Three-layer hierarchy designed for this (but repo status uncertain) |
| **Learning over time** | Hindsight | Mental Models self-update — only option with true reflection/learning |
| **Budget concern** | Built-in → Mem0 (free tier) → Hindsight (self-hosted Docker) | Ascending cost/complexity |

## Configuration Example

```yaml
# In ~/.hermes/config.yaml
memory:
  memory_enabled: true        # always on
  user_profile_enabled: true  # always on
  provider: mem0              # or '' (built-in), honcho, hindsight, etc.
  write_approval: false
  memory_char_limit: 2200
  user_char_limit: 1375
```

Setup command:
```bash
hermes memory setup   # interactive picker
hermes memory status  # see what's active
hermes memory off     # disable external provider
```

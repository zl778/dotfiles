---
name: hermes-memory
description: "Hermes Agent memory system — built-in MEMORY.md/USER.md, external memory providers (Honcho/Mem0/Hindsight/etc.), memory consolidation workflow, and provider comparison."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [memory, providers, consolidation, honcho, mem0, hindsight]
---

# Hermes Memory System

## Overview

Hermes Agent has a **multi-layer memory system**:

| Layer | Mechanism | Persistence | How it works |
|-------|-----------|-------------|-------------|
| L1 — `memory` tool | MEMORY.md + USER.md | ✅ Cross-session | Agent-managed compact notes; injected into system prompt at every session start |
| L2 — `session_search` | SQLite + FTS5 | ✅ Cross-session | Agent queries past conversation history on demand |
| L3 — Context compression | Current session only | ❌ Session-only | Auto-compresses long conversations (50% threshold → 20% target) |

MEMORY.md and USER.md live in `~/.hermes/memories/`. The agent manages them via the `memory` tool.

## Built-in Memory (MEMORY.md + USER.md)

Two files, injected frozen at session start:

| File | Purpose | Default limit |
|------|---------|--------------|
| MEMORY.md | Agent's personal notes — environment facts, conventions, lessons learned | 2,200 chars |
| USER.md | User profile — preferences, communication style, job background | 1,375 chars |

### Memory vs Skills Decision Framework

When deciding where to put information:

| Belongs in **MEMORY** | Belongs in **SKILL** |
|----------------------|---------------------|
| Environment facts (path layouts, tool locations, VPS IPs) | Step-by-step procedures |
| User conventions (naming rules, folder structure) | Reusable workflows with exact commands |
| Infrastructure details (domain names, Telegram IDs) | Multi-step processes with pitfalls |
| Constraint facts (.env protection, cannot-use notes) | Anything referenced across multiple sessions |

**Rule of thumb:** If it's "I need to know this to avoid asking" → memory. If it's "how to do X step by step" → skill.

### Memory Consolidation Workflow

When memory or user profile nears capacity:

1. **Audit**: List current entries. Flag candidates for removal:
   - Transient project status (deployed services list, in-progress work)
   - Procedures already covered by a SKILL.md
   - Duplicate info between MEMORY and USER
   - Rarely-used references (e.g. Obsidian URI syntax)

2. **Move to skills**: Extract step-by-step procedures from memory into a SKILL.md, then remove the procedure detail from memory (keep only the principle).

3. **Consolidate**: Batch-remove old entries, batch-add consolidated shorter versions in one `memory(operations=[...], target='memory')` call. Use `old_text` as a unique substring per entry.

4. **Verify**: Check usage percentage post-consolidation. Target <60% for headroom.

Common candidates to remove from memory:
- Apple Reminders osascript syntax (`apple-reminders` skill covers it)
- Obsidian CLI commands (`obsidian` skill covers it)
- Daily cron job config (`hermes-cron-jobs` skill covers it)
- Dotfiles sync steps (`dotfiles-setup` skill covers it)
- Word collector workflow (`word-collector` skill covers it)
- VPS deployed service list (changes too often)

### Configuration

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  write_approval: false       # false = agent can write without confirm
  memory_char_limit: 2200
  user_char_limit: 1375
  provider: ''                # '' = built-in only
  nudge_interval: 10
  flush_min_turns: 6
```

Increase limits:
```
hermes config set memory.memory_char_limit 4000
hermes config set memory.user_char_limit 2500
```

## External Memory Providers

Hermes ships with **8 built-in provider plugins** that work alongside the built-in memory. Only one external provider can be active at a time.

### Quick Start

```bash
hermes memory setup      # interactive picker + configuration
hermes memory status     # check active provider
hermes memory off        # disable external, fall back to built-in only
```

Or set manually in config.yaml:
```yaml
memory:
  provider: honcho   # or mem0, hindsight, openviking, holographic, retaindb, byterover, supermemory
```

### How Providers Work

When a provider is active, Hermes automatically:
1. Injects provider context into system prompt
2. Prefetches relevant memories before each turn (non-blocking)
3. Syncs conversation turns to provider after each response
4. Extracts memories on session end

### Provider Comparison

| Provider | Stars | Deployment | Dependencies | LongMemEval | Best for |
|----------|-------|------------|-------------|-------------|----------|
| **Built-in (SQLite)** | (Hermes core) | Zero — file-based | None | N/A | Simple needs, offline |
| **Honcho** | (repo deprecated?) | Plugin + PostgreSQL | DB server, plugin | ? | Multi-user isolation |
| **Mem0** | 59.7k | pip/npm + API key | API key (free tier) | **94.8** | Easy setup, strong retrieval |
| **Hindsight** | 17.8k | Docker or embedded | OpenAI API key, Docker | **SOTA** (independently verified) | Max accuracy, learning capability |

See `references/provider-comparison.md` for full detail.

### Recommendation by Use Case

| Your situation | Recommended |
|---------------|-------------|
| **Keep it simple, offline** | Built-in (just consolidated ✅) |
| **Want auto-extraction** | Mem0 (`hermes memory setup` → pick mem0) |
| **Need max accuracy** | Hindsight (Docker + API key) |
| **Multi-user/project isolation** | Honcho (if still available) |

## Pitfalls

- **Memory does NOT auto-compact.** When full, the tool returns an error — the agent must consolidate itself.
- **replace is also bound by the limit.** A longer replacement can overflow. Remove another entry first or shorten the new content.
- **External providers need the agent to stay online.** Built-in memory always works offline.
- **Only one external provider at a time.** Built-in memory is always active alongside it.
- **Provider context and memories are fetched per-turn**, adding latency vs built-in's zero-cost injection.
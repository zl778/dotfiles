---
name: cross-agent-memory
description: Understand and bridge memory systems across different coding agents (Hermes, Codex CLI, Claude Code, etc.). Covers each agent's memory architecture, limitations, and practical strategies for sharing context between them.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [memory, cross-agent, codex, claude-code, architecture, bridging]
    related_skills: [hermes-agent, codex, claude-code]
---

# Cross-Agent Memory

Different coding agents have fundamentally different memory architectures. This skill helps you understand each one and bridge them when running multiple agents side by side.

## When to use

- User asks "can Hermes and Codex share memory?"
- User asks "how does Codex remember things across sessions?"
- User runs multiple agents (Hermes + Codex, Hermes + Claude Code) and wants shared context
- Debugging why one agent doesn't know what another agent did
- Evaluating which memory provider to use for multi-agent setups

## Agent Memory Comparison

| Agent | Persistent Memory | Context Mechanism | External Provider Support |
|-------|-----------------|-------------------|-------------------------|
| **Hermes** | ✅ `memory` tool (MEMORY.md + USER.md) + SQLite session store | Skills (SKILL.md), system prompt injection | ✅ 8 built-in plugins (Hindsight, Mem0, Honcho…) |
| **Codex CLI** | ❌ None — only current thread context | `.codex/rules/*.mdc`, `AGENTS.md` (read at session start) | ❌ No built-in; can use MCP or AGENTS.md rules |
| **Claude Code** | ❌ None — only current conversation | `.claude/skills/*.mdc` (read at session start) | ❌ No built-in; can use MCP or skills rules |

## Bridging Strategies

See `references/codex-hermes-memory-bridging.md` for the detailed comparison of three approaches — including Codex's specific rules-file loading behavior, the Hermes-as-middleman workflow, and pitfalls like mid-session rule-file invisibility and Hindsight container uptime requirements.

### A: Shared Memory Service (Hindsight / Mem0)
Both agents connect to the same external memory service via API or MCP. Strongest retrieval quality. Requires a 24/7 service.

### B: File-Based Shared Context
Both agents read/write a shared markdown file at session start/end. Zero deployment, no extra services. Pure manual discipline.

### C: Hermes as Memory Middleman
Hermes delegates to Codex/Claude, sees their output, extracts key info, writes to its own memory. Fits existing workflows. No new infrastructure.

## Decision Table

| Criterion | A: Shared Service | B: Shared File | C: Middleman |
|-----------|-----------------|---------------|-------------|
| **Deployment** | Docker or cloud API | None | None |
| **Bidirectional?** | ✅ Yes | ✅ Yes | ❌ One-way (agent→Hermes) |
| **Retrieval quality** | 🏆 Semantic + entity + time | Plain text | Manual extract |
| **Auto sync** | ✅ Automatic | Manual read/write | Semi-automatic |
| **Works standalone** | ✅ Yes | ✅ Yes | ❌ Needs Hermes |

## Pitfalls

- **Codex has NO persistent memory.** Do not assume it remembers past sessions. Anything that needs to persist must be in rules/AGENTS.md or fetched via MCP at session start.
- **Rules files are read at session start only.** Mid-session changes to `.codex/rules/` are not picked up.
- **Hermes memory is unidirectional for middleman approach** — Codex sessions started outside Hermes (standalone `codex` in terminal) never sync.
- **Hindsight Docker needs 24/7 uptime** for shared-service approach. If the container stops mid-session, recall fails silently.
- **Mem0 API key** — the cloud tier has rate limits. Self-hosted Mem0 is available but needs its own infrastructure.

## Provider Comparison Reference

| Provider | GitHub ⭐ | Arch | Retrieval | Deployment |
|----------|----------|------|-----------|------------|
| Built-in SQLite | — (Hermes built-in) | Flat key-value entries | Full prompt injection | Zero |
| Hindsight | 17.8k | Biomimetic (Facts/Exp/Mental) | Semantic + entity + time (SOTA) | Docker (24/7) |
| Mem0 | 59.7k | Entity + BM25 + semantic | 94.8 LongMemEval | API key or self-hosted |
| Honcho | (repo unavailable) | User/session/agent layers | API query | PostgreSQL + service |
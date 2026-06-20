# Curator run — 2026-06-13T06:00:32.153712+00:00

Model: `(not resolved)` via `(not resolved)`  ·  Duration: 3s  ·  Agent-created skills: 63 → 63 (+0)

> ⚠ LLM pass error: `AIAgent import failed: cannot import name 'model_forces_max_completion_tokens' from 'utils' (/Users/liangzhu/.hermes/hermes-agent/utils.py)`

## Auto-transitions (pure, no LLM)

- checked: 63
- marked stale: 0
- archived (no LLM, pure time-based staleness): 0
- reactivated: 0

## LLM consolidation pass

- tool calls: **0** (by name: none)
- consolidated into umbrellas: **0**
- pruned (archived for staleness): **0**
- new skills this run: **0**
- state transitions (active ↔ stale ↔ archived): **0**

## Recovery

- Restore an archived skill: `hermes curator restore <name>`
- All archives live under `~/.hermes/skills/.archive/` and are recoverable by `mv`
- See `run.json` in this directory for the full machine-readable record.

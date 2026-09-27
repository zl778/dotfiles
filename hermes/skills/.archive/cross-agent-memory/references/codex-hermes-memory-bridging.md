# Codex ↔ Hermes Memory Bridging

Codex CLI has **no persistent memory system**. It relies entirely on its current thread's conversation context and startup-time rules files (`.codex/rules/*.mdc`, `AGENTS.md`).

Hermes has a full memory stack: `memory` tool (MEMORY.md + USER.md), SQLite session search (`session_search`), and 8 external memory provider plugins.

## Codex Context Sources

Codex reads these at **session start only** (mid-session changes are ignored):

| File | Location | Purpose |
|------|----------|---------|
| `AGENTS.md` | Project root | Project-level instructions, conventions, memory bank |
| `.codex/rules/*.mdc` | Project root | Skill-like markdown with frontmatter (equivalent to SKILL.md) |
| `CLAUD.md` / `CLAUDE.md` | Project root | Common aliases |
| `.github/copilot-instructions.md` | Project root | Also recognised |

## Three Approaches

### Approach A: Shared Memory Service (Hindsight / Mem0)

```
Hermes ──→ Hindsight Server (Docker) ←── Codex
```

**Hermes:** `memory.provider: hindsight` — built-in plugin, automatic sync of conversation turns and memory extraction.

**Codex:** No built-in provider. Two integration paths:

1. **Via AGENTS.md rule** — instruct Codex to fetch/push memory at session boundaries:
   ```markdown
   ## Memory sync
   At start, fetch recent memories: GET http://localhost:8888/api/v1/banks/shared/recall?query=<project>
   At end, retain key decisions: POST http://localhost:8888/api/v1/banks/shared/retain
   ```

2. **Via MCP** — if Hindsight exposes an MCP server (or you build a lightweight one), Codex loads it as a tool and calls retain/recall/reflect during the session.

**Tradeoffs:**
- ✅ Hermes integration is native
- ✅ Best retrieval quality (LongMemEval SOTA with Hindsight, 94.8 with Mem0)
- ⚠️ Codex integration is manual (rule-based, no built-in plugin)
- ⚠️ Docker container must run 24/7

### Approach B: Shared File

```bash
# e.g. ~/shared-memory/project-context.md
```

**Hermes:** Reference in a SKILL.md or system-prompt rule:
```
Load ~/shared-memory/project-context.md at session start.
Append key decisions at session end.
```

**Codex:** Reference in AGENTS.md or `.codex/rules/`:
```markdown
## Shared context
Read ~/shared-memory/project-context.md at session start.
Append outcomes before session end.
```

**Tradeoffs:**
- ✅ Zero deployment, zero extra services
- ✅ Both sides treat identically
- ⚠️ Manual discipline — no automatic sync
- ⚠️ Flat text only, no semantic retrieval
- ⚠️ No per-user/project access control

### Approach C: Hermes-as-Middleman (Already Working)

When Hermes delegates to Codex (`delegate_task` or `codex exec`), Hermes sees Codex's full output and can extract key information:

```
User → Hermes → delegates to Codex
                   ↓
           Codex executes → produces output
                   ↓
           Hermes extracts: files touched, decisions made, blockers
                   ↓
           Hermes writes summary to memory tool
```

**To enable:** After every Codex delegation, scan the output for:
- Files modified/created
- Architectural decisions
- Blockers encountered
- Remaining work

Write a concise summary via the `memory` tool so the next Hermes session starts knowing what Codex accomplished.

**Tradeoffs:**
- ✅ Fits existing delegation workflow
- ✅ No extra services
- ✅ Hermes controls retention policy
- ⚠️ One-way only (Codex→Hermes)
- ⚠️ Standalone `codex` terminal sessions don't sync

## Quick Decision

| Your scenario | Best approach |
|---------------|--------------|
| Already use Hermes to spawn Codex | **C: Middleman** — zero infra, add extract step |
| Run Codex standalone too | **A: Shared service** or **B: Shared file** |
| Want zero extra infra | **B: Shared file** |
| Want strongest retrieval + auto sync | **A: Hindsight/Mem0** |

## Pitfalls

- **Don't assume Codex remembers.** It has zero cross-session memory. Anything that must survive between sessions must be in rules/AGENTS.md or fetched via API/MCP.
- **Rules files are snapshotted.** Changes to `.codex/rules/` mid-session have no effect. Close and reopen Codex.
- **Hindsight container offline = silent fail.** No recall results returned, no error surface visible in the agent's conversation. Monitor container health.
- **File path with spaces.** macOS iCloud paths contain spaces. Use double-quoted absolute paths in AGENTS.md rules, never backslash-escaped inside quotes.
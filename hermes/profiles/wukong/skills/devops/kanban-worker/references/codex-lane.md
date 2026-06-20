# Codex Lane — Full Protocol for Kanban Workers

## Overview

This protocol defines the lightweight Hermes+Codex dual-lane convention for Kanban workers. Hermes is always the task owner: it decides whether Codex is appropriate, creates an isolated workspace, starts and monitors Codex, reconciles any diff, runs verification, and writes the final `kanban_complete` or `kanban_block` handoff. Codex is an input lane only.

## Mode Selection

Use `codex exec` for bounded one-shot edits where Codex should exit on its own:
```python
terminal(
    command="codex exec --full-auto '$(cat /tmp/codex_prompt.md)'",
    workdir=WORKTREE,
    background=True,
    pty=True,
    notify_on_complete=True,
)
```

Use Codex `--enable goals` for broader multi-step work that benefits from durable objective tracking. Launch with PTY.

## Required Worktree and Branch Pattern

```bash
TASK_ID="${HERMES_KANBAN_TASK:-t_manual}"
REPO="/path/to/repo"
BASE="$(git -C "$REPO" rev-parse --abbrev-ref HEAD)"
SAFE_TASK="$(printf '%s' "$TASK_ID" | tr -cd '[:alnum:]_-')"
BRANCH="codex/${SAFE_TASK}/$(date -u +%Y%m%d%H%M%S)"
WORKTREE="/tmp/${SAFE_TASK}-codex-lane"

git -C "$REPO" fetch --all --prune
git -C "$REPO" worktree add -b "$BRANCH" "$WORKTREE" "$BASE"
```

## Prompt Construction

Every Codex prompt must include:
- `task_id`, title, and full Kanban acceptance criteria
- Repo path, worktree path, branch name, allowed file scope
- Explicit: Hermes owns Kanban lifecycle; Codex is an input lane only
- Required output: concise summary, files changed, commits, tests run, known risks
- Prohibited: secrets access, external messaging, board mutation, unrelated refactors
- Verification commands Codex may run and commands Hermes will run afterward

## Reconciliation Checklist

Before accepting any Codex lane result:
- [ ] `git status --short --branch` shows only expected files
- [ ] `git diff --stat` reviewed by Hermes
- [ ] No secrets, credentials, generated caches, or local artifacts included
- [ ] Safety constraints preserved
- [ ] Codex commits are small enough to cherry-pick cleanly
- [ ] Hermes ran canonical tests itself
- [ ] Accepted commits/diffs applied to Hermes-owned workspace

## kanban_complete Metadata Schema

```json
{
  "codex_lane": {
    "used": true,
    "mode": "exec | goal | skipped",
    "worktree": "/absolute/path",
    "branch": "codex/t_caa69668/20260508100000",
    "result": "accepted | rejected | partial | timed_out",
    "accepted_commits": ["<sha>"],
    "rejected_reason": "concrete reason",
    "tests_run": [{"command": "...", "exit_code": 0, "owner": "hermes"}]
  }
}
```

## Common Pitfalls

1. Treating Codex self-report as verification — always inspect the diff and rerun tests
2. Running Codex in a dirty main checkout — always isolate in a worktree
3. Letting Codex own Kanban state — Codex may summarize, Hermes writes board state
4. Killing a stuck lane without recording why — `rejected_reason` must explain the decision
5. Using `/goal` for quick edits — prefer `codex exec` unless multi-step continuation needed

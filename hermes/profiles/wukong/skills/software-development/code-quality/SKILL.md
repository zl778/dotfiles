---
name: code-quality
description: "TDD (test-driven development) methodology and pre-commit code review/verification pipeline."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [testing, tdd, code-review, security, quality, red-green-refactor, verification]
    related_skills: [debugging, planning-and-spiking, subagent-driven-development]
---

# Code Quality

## Overview

Two complementary quality disciplines:

- **Test-Driven Development** — write the test first, watch it fail, then implement
- **Pre-Commit Code Verification** — automated verification pipeline before code lands

**Core principle:** No agent should verify its own work. Fresh context finds what you miss. If you didn't watch the test fail, you don't know if it tests the right thing.

## When to Use

| Mode | When |
|------|------|
| TDD | New features, bug fixes, refactoring, behavior changes |
| Code Review | After implementing, before `git commit` or `git push` |

**Always use both** for new code. Skip TDD only for throwaway prototypes, generated code, or config files (ask first).

---

## Section A: Test-Driven Development

### The Iron Law
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over. No exceptions.

### Red-Green-Refactor Cycle

#### RED — Write Failing Test

Write one minimal test showing what should happen:
```python
def test_retries_failed_operations_3_times():
    attempts = 0
    def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise Exception('fail')
        return 'success'
    result = retry_operation(operation)
    assert result == 'success'
    assert attempts == 3
```

Requirements: one behavior per test, clear descriptive name, real code not mocks.

#### Verify RED — Watch It Fail

**MANDATORY. Never skip.**
```bash
pytest tests/test_feature.py::test_specific_behavior -v
```
Confirm: test fails for expected reason (feature missing, not typo).

#### GREEN — Minimal Code

Write the simplest code to pass the test. Nothing more. Cheating is OK (hardcode, copy-paste, skip edge cases — fix in REFACTOR).

#### Verify GREEN — Watch It Pass

**MANDATORY.**
```bash
pytest tests/test_feature.py::test_specific_behavior -v
pytest tests/ -q   # check for regressions
```

#### REFACTOR — Clean Up

Remove duplication, improve names, extract helpers. Keep tests green throughout.

### Why Order Matters

- Tests written after code pass immediately → prove nothing
- Test-first forces you to see the test fail → proves it tests something
- Tests-after = "what does this do?" Tests-first = "what should this do?"

### Common Rationalizations (and why they're wrong)

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keep it and risk bugs. |
| "TDD will slow me down" | TDD is faster than debugging. |

### Red Flags — STOP and Start Over

- Code before test. Test after implementation. Test passes immediately.
- Rationalizing "just this once." All mean: Delete code. Start over with TDD.

---

## Section B: Pre-Commit Code Verification

Automated pipeline before code lands: static scans, baseline-aware quality gates, independent reviewer subagent, and auto-fix loop.

### Step 1 — Get the Diff
```bash
git diff --cached
```
If empty, try `git diff` then `git diff HEAD~1 HEAD`. If still empty → nothing to verify.

### Step 2 — Static Security Scan

```bash
# Hardcoded secrets
git diff --cached | grep "^+" | grep -iE "(api_key|secret|password|token)\s*=\s*['\"][^'\"]{6,}['\"]"
# Shell injection, dangerous eval/exec, unsafe deserialization, SQL injection
```

### Step 3 — Baseline Tests and Linting

Detect project language, run appropriate tools. Compare against baseline (stash → run → pop). Only NEW failures block the commit.

```bash
# Python
python -m pytest --tb=no -q 2>&1 | tail -5
which ruff && ruff check . 2>&1 | tail -10
```

### Step 4 — Self-Review Checklist
- [ ] No hardcoded secrets, API keys, or credentials
- [ ] Input validation on user-provided data
- [ ] SQL queries use parameterized statements
- [ ] No debug print/console.log left behind
- [ ] New code has tests (if test suite exists)

### Step 5 — Independent Reviewer Subagent

Call `delegate_task` with git diff and static scan results. The reviewer has NO shared context with the implementer.

```python
delegate_task(
    goal="You are an independent code reviewer. Review the git diff and return ONLY valid JSON.",
    context="""FAIL-CLOSED: security_concerns non-empty → passed=false.
logic_errors non-empty → passed=false. Only set passed=true when both are empty.
Return JSON: {"passed": bool, "security_concerns": [], "logic_errors": [], "suggestions": [], "summary": "..."}""",
    toolsets=["terminal"]
)
```

### Step 6 — Evaluate Results

All passed → commit. Any failures → report, then auto-fix.

### Step 7 — Auto-Fix Loop (max 2 cycles)

Spawn a fix agent that fixes ONLY the reported issues, then re-verify.

### Step 8 — Commit
```bash
git add -A && git commit -m "[verified] <description>"
```

### Integration with Other Skills

- **subagent-driven-development:** Run after each task as quality gate
- **test-driven-development:** Verifies TDD discipline was followed
- **planning-and-spiking:** Validates implementation matches plan

---

## References

| File | Description |
|------|-------------|
| `references/tdd-detailed.md` | Full TDD methodology with expanded rationalizations and anti-patterns |
| `references/pre-commit-review-detailed.md` | Full pre-commit review pipeline with language-specific scan patterns |

## Common Pitfalls

1. **Skipping TDD** because "it seems simple" — simple bugs have root causes too
2. **Empty diff** — check `git status`, tell user nothing to verify
3. **Large diff (>15k chars)** — split by file, review each separately
4. **`delegate_task` returns non-JSON** — retry once, then treat as FAIL
5. **Auto-fix introduces new issues** — counts as a new failure, cycle continues
6. **pdb under xdist** — pdb silently does nothing under xdist

## Verification Checklist

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass, output pristine
- [ ] No hardcoded secrets in diff
- [ ] No regressions vs baseline
- [ ] Independent reviewer approved
- [ ] `[verified]` prefix in commit message

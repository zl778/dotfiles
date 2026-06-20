# Root Cause Debugging Methodology — Expanded Reference

## The Four Phases — Detailed

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - Read stack traces completely — note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?

3. **Check Recent Changes**
   ```bash
   git log --oneline -10
   git diff
   git log -p --follow src/problematic_file.py | head -100
   ```

4. **Gather Evidence in Multi-Component Systems**
   For each component boundary: log what enters, what exits, verify environment/config propagation.

5. **Trace Data Flow**
   - Where does the bad value originate?
   - Trace upstream until you find the source
   - Fix at the source, not the symptom

### Phase 2: Pattern Analysis

1. Find working examples in the same codebase
2. Compare against reference implementations — read COMPLETELY, don't skim
3. Identify every difference between working and broken
4. Understand dependencies, config, environment, assumptions

### Phase 3: Hypothesis and Testing

1. Form a single hypothesis: "I think X is root cause because Y"
2. Make the SMALLEST possible change to test it
3. One variable at a time
4. Verify before continuing

### Phase 4: Implementation

1. Create a failing test case first (RED)
2. Fix the root cause — ONE change at a time
3. Verify fix — run tests, check for regressions
4. The Rule of Three:
   - < 3 fixes: Return to Phase 1 if still failing
   - ≥ 3 fixes failed: STOP and question the architecture
   - Discuss with user before more attempts

## Red Flags

If you catch yourself thinking ANY of these, STOP and return to Phase 1:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "I don't fully understand but this might work"
- "One more fix attempt" (when 2+ already failed)
- Proposing solutions before tracing data flow

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time" | Systematic debugging is FASTER than guessing. |
| "Just try this first" | First fix sets the pattern. Do it right from the start. |
| "Multiple fixes saves time" | Can't isolate what worked. Causes new bugs. |
| "One more fix" (after 2+ failures) | 3+ failures = architectural problem. |

## When 3+ Fixes Failed — Question Architecture

**Pattern indicating architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Should we refactor vs. continue fixing symptoms?

## Hermes Tool Integration

| Phase | Tools |
|-------|-------|
| 1. Root Cause | `search_files`, `read_file`, `terminal` (repro, git), `web_search`/`web_extract` |
| 2. Pattern | `search_files` (find similar), `read_file` (compare) |
| 3. Hypothesis | `terminal` (run test), `execute_code` (quick prototype) |
| 4. Implementation | `patch`, `write_file`, `terminal` (pytest) |

For complex multi-component debugging, use `delegate_task` with `systematic-debugging` context.

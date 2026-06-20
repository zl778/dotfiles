# Writing Implementation Plans — Expanded Reference

## Full Task Template

```markdown
### Task N: [Descriptive Name]

**Objective:** One sentence

**Files:**
- Create: `exact/path/to/new_file.py`
- Modify: `exact/path/to/existing.py:45-67`
- Test: `tests/path/to/test_file.py`

**Step 1: Write failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify failure**
Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: FAIL — "function not defined"

**Step 3: Write minimal implementation**
```python
def function(input):
    return expected
```

**Step 4: Run test to verify pass**
Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: PASS

**Step 5: Commit**
```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## Task Ordering

1. Setup/infrastructure
2. Core functionality (TDD for each)
3. Edge cases
4. Integration
5. Cleanup/documentation

## Principles

### DRY (Don't Repeat Yourself)
Bad: Copy-paste validation in 3 places
Good: Extract validation function, use everywhere

### YAGNI (You Aren't Gonna Need It)
Bad: Add "flexibility" for future requirements
Good: Implement only what's needed now

### TDD for every code task
1. Write failing test
2. Run to verify failure
3. Write minimal code
4. Run to verify pass

## Common Mistakes

- Vague tasks: "Add authentication" → "Create User model with email and password_hash fields"
- Incomplete code: include the actual code, not "add validation"
- Missing verification: exact command + expected output
- Missing file paths: "the model file" → "`src/models/user.py`"

## Execution Handoff

After saving the plan, offer: "Plan complete. Ready to execute using subagent-driven-development — I'll dispatch a fresh subagent per task with two-stage review."

When executing, use `subagent-driven-development` skill:
- Fresh `delegate_task` per task with full context
- Spec compliance review after each task
- Code quality review after spec passes

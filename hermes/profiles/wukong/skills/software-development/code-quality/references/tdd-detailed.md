# TDD — Expanded Reference

## Full RED-GREEN-REFACTOR Cycle

### RED — Write Failing Test

**Good test:**
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

**Bad test:**
```python
def test_retry_works():
    mock = MagicMock()
    mock.side_effect = [Exception(), Exception(), 'success']
    result = retry_operation(mock)
    assert result == 'success'  # What about retry count? Timing?
```

### Verify RED — Watch It Fail
**MANDATORY. Never skip.**
```bash
pytest tests/test_feature.py::test_specific_behavior -v
```

### GREEN — Minimal Code
Write the simplest code to pass the test. Nothing more.
```python
def add(a, b):
    return a + b  # No logging, no extra features
```

### Verify GREEN — Watch It Pass
**MANDATORY.**
```bash
pytest tests/test_feature.py::test_specific_behavior -v
pytest tests/ -q  # check regressions
```

### REFACTOR — Clean Up
- Remove duplication, improve names, extract helpers
- Keep tests green throughout
- Don't add behavior

## Hermes Tool Integration

```python
# RED — verify failure
terminal("pytest tests/test_feature.py::test_name -v")

# GREEN — verify pass
terminal("pytest tests/test_feature.py::test_name -v")

# Full suite — verify no regressions
terminal("pytest tests/ -q")
```

## With delegate_task
```python
delegate_task(
    goal="Implement [feature] using strict TDD",
    context="Follow testing skill: 1. Write failing test FIRST. 2. Run to verify fail. 3. Write minimal code. 4. Run to verify pass. 5. Refactor if needed. 6. Commit.",
    toolsets=['terminal', 'file']
)
```

## With systematic-debugging
Bug found? Write failing test reproducing it. Follow TDD cycle. The test proves the fix and prevents regression.

## Testing Anti-Patterns
- Testing mock behavior instead of real behavior
- Testing implementation details (test behavior/results)
- Happy path only (always test edge cases, errors, boundaries)
- Brittle tests (test behavior, not structure)

## Verification Checklist
- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass, output pristine
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

## When Stuck
| Problem | Solution |
|---------|----------|
| Don't know how to test | Write the wished-for API. Write the assertion first. |
| Test too complicated | Design too complicated. Simplify the interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify the design. |

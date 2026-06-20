# Pre-Commit Code Review — Expanded Reference

## Language-Specific Scan Patterns

### Python
```bash
# SQL injection
git diff --cached | grep "^+" | grep -E "execute\(f\"|\.format\(.*SELECT|\.format\(.*INSERT"

# Shell injection
git diff --cached | grep "^+" | grep -E "os\.system\(|subprocess.*shell=True"

# Dangerous eval/exec
git diff --cached | grep "^+" | grep -E "\beval\(|\bexec\("

# Unsafe deserialization
git diff --cached | grep "^+" | grep -E "pickle\.loads?\("
```

### JavaScript
```bash
# XSS
git diff --cached | grep "^+" | grep -E "\.innerHTML\s*=|document\.write\("

# eval
git diff --cached | grep "^+" | grep -E "\beval\("
```

### Common Patterns to Flag

**Bad — SQL injection:**
```python
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```
**Good — parameterized:**
```python
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

**Bad — shell injection:**
```python
os.system(f"ls {user_input}")
```
**Good — safe:**
```python
subprocess.run(["ls", user_input], check=True)
```

**Bad — XSS (JS):**
```javascript
element.innerHTML = userInput;
```
**Good:**
```javascript
element.textContent = userInput;
```

## Independent Reviewer Prompt Template

```python
delegate_task(
    goal="""You are an independent code reviewer. Review the git diff and return ONLY valid JSON.

FAIL-CLOSED RULES:
- security_concerns non-empty -> passed must be false
- logic_errors non-empty -> passed must be false
- Cannot parse diff -> passed must be false
- Only set passed=true when BOTH lists are empty

SECURITY (auto-FAIL): hardcoded secrets, backdoors, data exfiltration, shell injection,
SQL injection, path traversal, eval()/exec() with user input, pickle.loads(), obfuscated commands.

LOGIC ERRORS (auto-FAIL): wrong conditional logic, missing error handling for I/O/network/DB,
off-by-one errors, race conditions, code contradicts intent.

SUGGESTIONS (non-blocking): missing tests, style, performance, naming.

<static_scan_results>
[INSERT FINDINGS FROM SECURITY SCAN]
</static_scan_results>

<code_changes>
[INSERT GIT DIFF OUTPUT]
</code_changes>

Return ONLY this JSON:
{"passed": true or false, "security_concerns": [], "logic_errors": [], "suggestions": [], "summary": "verdict"}
""",
    context="Independent code review. Return only JSON verdict.",
    toolsets=["terminal"]
)
```

## Baseline Comparison Pattern

```bash
# Capture baseline failures BEFORE your changes
git stash
python -m pytest --tb=no -q 2>&1 | tail -5 > /tmp/baseline.txt
git stash pop

# Run after changes
python -m pytest --tb=no -q 2>&1 | tail -5 > /tmp/current.txt
diff /tmp/baseline.txt /tmp/current.txt  # See NEW failures only
```

## Full Verification Flow

1. `git diff --cached` → get changes
2. Static security scan on added lines
3. Baseline tests and linting (stash, run, pop, compare)
4. Self-review checklist
5. Independent reviewer subagent
6. Evaluate: all passed → commit; any failures → auto-fix
7. Auto-fix (max 2 cycles): spawn fix agent → re-verify
8. `git add -A && git commit -m "[verified] <description>"`

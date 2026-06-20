---
name: planning-and-spiking
description: "Write implementation plans, run spikes/experiments, produce ideation prompts, and generate markdown plans without execution."
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [planning, spike, ideation, prototype, implementation, workflow, design, exploration, brainstorming]
    related_skills: [subagent-driven-development, test-driven-development, code-quality]
---

# Planning, Ideation, and Spiking

## Overview

Four complementary workflows for the creative and planning phases of development:

- **Ideation** — generate project ideas through creative constraints when the user has tools but no direction
- **Writing Plans** — comprehensive implementation plans for multi-step features, assuming the implementer has zero context
- **Plan Mode** — produce a markdown plan without executing any code (read-only investigation)
- **Spiking** — throwaway experiments to validate an idea before committing to a real build

**Core principle:** A good plan makes implementation obvious. If someone has to guess, the plan is incomplete.

## When to Use

| Mode | When |
|------|------|
| Ideation | User says "I want to build something", "give me a project idea", "I'm bored" |
| Writing Plans | Before implementing multi-step features, delegating to subagents |
| Plan Mode | User asks for a plan without execution (`/plan`) |
| Spike | Validating feasibility, comparing approaches, surfacing unknowns |

---

## Section A: Creative Ideation

Use when the user says "I want to build something", "give me a project idea", "I'm bored", "what should I make", or "inspire me". Works for code, art, hardware, writing, tools — anything that can be made.

### How It Works

1. **Pick a constraint** from the library below — random, or matched to the user's domain/mood
2. **Interpret it broadly** — a coding prompt can become a hardware project, an art prompt can become a CLI tool
3. **Generate 3 concrete project ideas** that satisfy the constraint
4. **If they pick one, build it** — create the project, write the code, ship it

### The Rule

Every prompt is interpreted as broadly as possible. "Does this include X?" → Yes. The prompts provide direction and mild constraint. Without either, there is no creativity.

### Constraint Library

**For Developers:**
- **Solve your own itch** — Build the tool you wished existed this week. Under 50 lines. Ship it today.
- **Automate the annoying thing** — What's the most tedious part of your workflow? Script it away.
- **The CLI tool that should exist** — `git undo-that-thing-i-just-did`. `docker why-is-this-broken`. Build it.
- **Nothing new except glue** — Make something entirely from existing APIs, libraries, and datasets.
- **Frankenstein week** — Take something that does X and make it do Y. A git repo that plays music.
- **Subtract** — How much can you remove before it breaks? Strip to minimum viable function.
- **High concept, low effort** — A deep idea, lazily executed. Should take an afternoon.

**For Makers & Artists:**
- **Blatantly copy something** — Recreate something you admire from scratch.
- **One million of something** — One million pixels, API calls, anything. Becomes interesting at scale.
- **Make something that dies** — A website that loses a feature every day. A chatbot that forgets.
- **Do a lot of math** — Generative geometry, shader golf, computational origami.

**For Anyone:**
- **Text is the universal interface** — No buttons, just words in and words out.
- **Start at the punchline** — Think of a funny sentence. Work backwards to make it real.
- **Hostile UI** — Make something intentionally painful to use.
- **Take two** — Rebuild an old project from scratch without looking at the original.

### Matching Constraints to Users

| User says | Pick from |
|-----------|-----------|
| "I want to build something" (no direction) | Random — any constraint |
| "I'm learning [language]" | Blatantly copy something, Automate the annoying thing |
| "I want something weird" | Hostile UI, Frankenstein week, Start at the punchline |
| "I want something useful" | Solve your own itch, The CLI tool, Automate the annoying thing |
| "I'm burned out" | High concept low effort, Make something that dies |
| "Weekend project" | Nothing new except glue, Start at the punchline |

### Output Format

```
## Constraint: [Name]
> [The constraint, one sentence]

### Ideas

1. **[One-line pitch]**
   [2-3 sentences: what you'd build and why it's interesting]
   ⏱ [weekend / week / month] • 🔧 [stack]

2. ...
```

See `references/full-ideation-prompt-library.md` for 30+ additional constraints across communication, scale, philosophy, transformation, and more. (Available at the ideation skill reference once saved.)

---

## Section B: Writing Implementation Plans

Use this when building features, breaking down complex requirements, or delegating to subagents.

### Bite-Sized Task Granularity

**Each task = 2-5 minutes of focused work.** Every step is one action:

- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement minimal code to pass" — step

### Plan Document Structure

Every plan starts with:
```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence]
**Architecture:** [2-3 sentences]
**Tech Stack:** [Key technologies]
---
```

Each task follows:
```
### Task N: [Descriptive Name]
**Objective:** One sentence
**Files:** Create/Modify/Test paths
**Steps:** 1-5 with exact commands and expected output
```

### Writing Process

1. Understand requirements (feature requirements, acceptance criteria, constraints)
2. Explore the codebase (`search_files`, `read_file`, check existing tests)
3. Design approach (architecture pattern, file organization, testing strategy)
4. Write tasks in order: setup → core (TDD) → edge cases → integration → cleanup
5. Include exact file paths, complete code, exact commands with expected output
6. Review: sequential? bite-sized? file paths exact? code copy-pasteable?

### Save Location
```bash
mkdir -p docs/plans
# Save to docs/plans/YYYY-MM-DD-feature-name.md
```

### Principles

- **DRY**: Extract shared logic, don't copy-paste
- **YAGNI**: Implement only what's needed now
- **TDD**: Write failing test first, then implement (see `code-quality` skill)
- **Frequent commits**: After every task

See `references/writing-plans.md` for the full expanded methodology with task templates, code examples, and execution handoff.

---

## Section C: Plan Mode

Use this when the user wants a plan instead of execution. `/plan` in-session triggers this mode.

### Core Behavior

- Do NOT implement code
- Do NOT edit project files except the plan markdown file
- Do NOT run mutating terminal commands, commit, push
- May inspect the repo with read-only commands
- Deliverable: a markdown plan saved to `.hermes/plans/`

### Output Requirements

Include, when relevant:
- Goal
- Current context / assumptions
- Proposed approach
- Step-by-step plan
- Files likely to change
- Tests / validation
- Risks, tradeoffs, open questions

### Save Location
```bash
.hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md
```

### Interaction Style

- If clear enough, write the plan directly
- If underspecified, ask a brief clarifying question
- After saving, reply with what you planned and the path

---

## Section D: Spiking — Throwaway Experiments

Use when the user wants to feel out an idea before committing — validating feasibility, comparing approaches.

### When NOT to Spike

- The answer is knowable from docs — just research
- The work is production path — use Section B (Writing Plans)
- The idea is already validated — jump to implementation

### Core Method

```
decompose → research → build → verdict
```

### 1. Decompose

Break the idea into 2-5 independent feasibility questions. Each is one spike. Order by risk — the most likely to kill the idea runs first.

| # | Spike | Validates (Given/When/Then) | Risk |
|---|-------|----------------------------|------|
| 001 | websocket-streaming | Given a WS, when LLM streams, then client receives <100ms | High |

### 2. Research (per spike)

Surface competing approaches, pick one, state why.

### 3. Build

One directory per spike. Bias toward something the user can interact with — a runnable CLI, minimal HTML page, or small web server.

```
spikes/
├── 001-websocket-streaming/
│   ├── README.md
│   └── main.py
```

**Depth over speed.** Never declare "it works" after one happy-path run. Test edge cases.

For parallel comparison spikes, use `delegate_task`:
```python
delegate_task(tasks=[
    {"goal": "Build 002a-approach-a: ...", "toolsets": ["terminal", "file", "web"]},
    {"goal": "Build 002b-approach-b: ...", "toolsets": ["terminal", "file", "web"]},
])
```

### 4. Verdict

Each spike's README closes with:

```markdown
## Verdict: VALIDATED | PARTIAL | INVALIDATED
### What worked
### What didn't
### Surprises
### Recommendation
```

### Comparison Spikes

When two approaches answer the same question, do a head-to-head:

```markdown
## Head-to-head: pdfjs vs camelot
| Dimension | pdfjs | camelot |
|-----------|-------|---------|
| Quality | 9/10 | 7/10 |
| Setup | npm install | pip + ghostscript |
```

## Common Pitfalls

1. **Vague tasks** — "Add authentication" → "Create User model with email and password_hash fields"
2. **Incomplete code** — include the actual code, not "add validation"
3. **Missing verification** — exact commands with expected output
4. **Skipping research** — research enough to pick the right approach
5. **No verdict** — every spike must end with VALIDATED/PARTIAL/INVALIDATED
6. **Treating first draft as sacred** — revision is creation
7. **Spikes that are too broad** — break into independent feasibility questions
8. **Keeping spike code** — a spike that takes 2 days to "clean up" was a bad spike
9. **No project direction** — pick a constraint before ideating, not any constraint

## Verification Checklist

- [ ] Plan has bite-sized tasks (2-5 min each)
- [ ] File paths are exact
- [ ] Code examples are complete (copy-pasteable)
- [ ] Commands are exact with expected output
- [ ] Verification steps included
- [ ] DRY, YAGNI, TDD applied
- [ ] Plan saved to proper location
- [ ] Spike has clear Given/When/Then framing
- [ ] Spike has verdict documented
- [ ] Spike code is disposable
- [ ] Ideation constraint matches user's mood/domain
- [ ] 3 concrete project ideas generated

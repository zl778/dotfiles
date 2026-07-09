# Multi-Agent Routing Reference

This reference complements the `multi-agent-orchestration` skill with a compact routing cheat sheet.

## What each dimension means

- Role = what the task needs.
- Instance = where the task runs.
- Channel = how the user interacts.

## Minimal worker registry fields

- name
- roles
- host / environment
- profile
- entry command / transport
- model preference and fallback
- return format
- availability

## Dispatch flow

1. Identify the task role.
2. Filter workers that can do the role.
3. Choose the best environment.
4. Check availability.
5. Dispatch.
6. Merge results in the master agent.

## Practical routing examples

- Coding bug fix → coding worker with strong code model
- Windows / SSH / Docker work → Windows or WSL execution worker
- Research / summarization → research worker
- Writing / summarizing the results → writing worker

## Example task intake

- What should be done?
- What result is expected?
- What constraints apply?
- What output format is needed?
- Should the master split this into subtasks?

## Session-specific reminders

- Keep the user-facing channel separate from execution nodes.
- A Telegram group can be the front door without requiring every worker to join it.
- When a new topic would muddy the current thread, split with `/new` or `/branch` instead of mixing topics.
- Use `/queue` for same-topic follow-up ideas and `/steer` for a light mid-turn correction.
- Kanban dispatch only spawns assigned profiles that actually exist on disk; a conceptual assignee name that is not a real profile will be skipped.

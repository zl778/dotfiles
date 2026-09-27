# User Multi-Agent Routing Notes

This note captures the user's preferred operating model for Hermes-style multi-agent work.

## Core distinction

- **Logical roles** answer: what kind of work is needed?
  - Researcher, Engineer, Navigator, Operator, Writer, Reviewer, Tester, Archivist, Scheduler
- **Worker nodes / instances** answer: where should the work run?
  - Mac Hermes, Win11 Hermes, WSL Hermes, wukong, or future nodes

## User preference

The user prefers a single main Hermes as the only conversational entry point. Sub-agents should be treated as backend executors rather than separate front-door interfaces.

## Interaction modes

- Telegram: mobile / outside-the-desk task handoff
- cmux: multi-terminal desk execution
- Hermes desktop/dashboard: overview, task organization, and cleanup

## Practical routing rule

1. User talks only to Hermes.
2. Hermes classifies the task by role.
3. Hermes routes the task to the best worker node.
4. Worker returns a concise result.
5. Main Hermes summarizes and closes the loop.

## Worker registry fields

When maintaining workers, keep these fields:
- name
- role
- host / node
- entry command
- capabilities
- return format
- status

## Model allocation

Keep a separate model allocation table so different workers can use different models for cost / speed / quality tradeoffs.

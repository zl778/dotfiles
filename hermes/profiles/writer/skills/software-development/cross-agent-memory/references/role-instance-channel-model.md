# Role / Instance / Channel Model

This note captures a practical pattern for Hermes-style multi-agent setups.

## Core distinctions

- Role: what the agent is doing (Research, Coding, Browser, Ops).
- Instance: where/how the agent runs (Mac Hermes, Win11 Hermes, WSL Hermes, wukong process).
- Channel/UI: how the user talks to the system (Telegram, cmux, desktop app/Kanban).
- Profile: isolated config/state/memory namespace for a Hermes installation.

## Recommended default

- Keep one master entry point for the user.
- Treat Research/Coding/Browser as logical roles first.
- Only create separate instances when there is a real need for:
  - parallel execution,
  - tool/permission isolation,
  - environment isolation,
  - different model/provider choice,
  - or independent uptime.

## Practical mapping from the session

- Telegram: mobile/external interaction mode when away from the computer.
- cmux: multi-window execution mode when actively working in terminal/CLI.
- Hermes desktop: overview and task management mode for review, organization, and consolidation.

These are not competing architectures; they are different working modes for the same overall system.

## Queueing rule of thumb

- Same task with a new detail -> queue/steer it into the current task.
- Independent new task -> start a separate task/session/worker.
- Low-priority idea -> log it to an inbox, do not interrupt.

## Telegram group rule

If a master agent handles dispatch, do not add every worker agent to the Telegram group by default. Keep the group focused on the master entry point unless a worker must speak to the user directly.
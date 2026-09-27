# Hermes Multi-Agent Orchestration Notes

This note captures the practical patterns discussed for Hermes-centric multi-agent setups.

## Core distinctions

- Role: what the agent does (Researcher, Engineer, Navigator, Operator, Writer)
- Instance: where it runs (Mac Hermes, wukong, Win11 Hermes, WSL Hermes)
- Interface: how the user talks to the system (Telegram, cmux, Hermes desktop)

## Recommended operating model

- User talks only to the main Hermes agent.
- Main Hermes does not perform all work itself; it routes tasks to workers.
- Workers should have a registry entry describing name, role, location, entry command, and return format.
- The user should not need to directly interact with every worker.

## Worker registry fields

- name
- role
- host / location
- entry method (SSH, local profile, cmux session, bot)
- capabilities
- busy / available status
- return format

## Task intake template

1. What do you want done?
2. What result should be achieved?
3. What constraints matter?
4. What output format do you want?

## When to split into separate agents

Split only when the task benefits from:
- parallelism
- permission separation
- tool separation
- context isolation
- specialist behavior

Do not split just because the task can be described with multiple labels.

## Practical user-facing modes

- Telegram: mobile / out-of-office interaction
- cmux: local multi-terminal execution and simultaneous control
- Desktop Hermes: task overview, consolidation, and整理

## Good default

Start with one main Hermes and a small set of workers. Expand only when the routing or concurrency pressure makes the split worthwhile.

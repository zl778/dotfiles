# Current worker registry notes (session snapshot)

This reference captures the current pattern used in the conversation:

## Current profiles / workers

- default — main coordinator, running
- wukong — running, high-frequency coding assistant
- researcher — stopped, on-demand research/synthesis worker
- engineer — stopped, on-demand coding/debug worker
- navigator — stopped, on-demand browser interaction worker
- operator — stopped, on-demand system/terminal/WSL/SSH/Docker worker
- writer — stopped, on-demand documentation/summarization worker

## Semantics clarified in this session

- `stopped` does NOT mean unusable.
- A stopped Hermes profile can still be invoked on demand with `hermes -p <profile> chat -q ...`.
- `running` means the gateway is already up and the profile is hot.
- Use running profiles for frequently used roles; keep task-shaped roles on demand when resource pressure matters.

## Practical routing rule of thumb

- Always-on: default, wukong
- On-demand: researcher, engineer, navigator, operator, writer
- Promote engineer to always-on only if daily usage is high enough to justify the extra background process

## Worker registry fields to keep in Obsidian

- name
- role
- host
- profile
- entry
- capabilities
- unsuitable_for
- return_format
- status
- notes

## Obsidian notes created in this session

- Hermes-worker通讯录模板.md
- Hermes-worker通讯录精简版.md
- 主Hermes读取worker通讯录的使用规范.md
- Hermes-worker角色落地清单.md
- Hermes-profile常驻与按需启动方案.md

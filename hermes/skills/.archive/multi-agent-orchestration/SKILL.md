---
name: multi-agent-orchestration
description: Design and operate a Hermes-style multi-agent system with a master coordinator, worker registry, kanban dispatch, model-per-agent routing, and clear separation between role, instance, and channel.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [multi-agent, orchestration, worker-registry, kanban, routing, models, telegram, cmux, dashboard]
    related_skills: [cross-agent-memory, hermes-agent, obsidian]
---

# Multi-Agent Orchestration

Use this skill when a user wants a Hermes-style system with one master agent and multiple workers across machines, profiles, models, and channels.

## When to use

- The user wants one entry point that delegates work to workers
- The user asks how to combine Mac, Windows, WSL, and local profiles into one system
- The user wants workers to use different models for cost/performance reasons
- The user wants Telegram, terminal/cmux, and dashboard to serve different interaction modes
- The user asks how Kanban, memory, and worker routing should fit together

## Core mental model

Keep three dimensions separate:

- **Role** = what the agent does
  - Examples: Planner, Researcher, Engineer, Navigator, Writer, Operator, Reviewer
- **Instance** = where it runs
  - Examples: Mac Hermes, Win11 Hermes, WSL Hermes, wukong profile/process
- **Channel** = how the user interacts with the system
  - Examples: Telegram, cmux/terminal, Hermes dashboard

Do not collapse these into one thing. A worker can have the same role as another worker while running in a different instance or being reached through a different channel.

## Recommended architecture

### 1. Master agent
The master agent is the only user-facing coordinator. It:
- accepts the task from the user
- decides whether the task needs to be split
- routes sub-tasks to workers
- merges the outputs
- writes durable knowledge back to memory or notes

### 2. Worker registry
Maintain a small explicit registry for workers. Each entry should include:
- name
- role(s)
- host / environment
- profile name
- entry command or transport
- model preference and fallback
- return format
- current availability

### 3. Kanban for state
Use Kanban to represent task state, not long-term knowledge.
Typical states:
- triage
- todo / ready
- running
- blocked
- done
- archived

### 4. Memory for durable facts
Use memory for stable facts, preferences, environment notes, and reusable procedures.
Do not use memory as a task queue.

## Routing rules

Route in this order:

1. Determine the role needed by the task.
2. Determine which worker instances can actually execute that role.
3. Prefer the best-fit environment.
4. Check current availability / load.
5. Dispatch to the chosen worker.
6. Merge results in the master agent.

## Worker selection heuristics

- **Research work** → worker with web/document access and strong summarization
- **Coding work** → worker with the strongest code model and repo access
- **Browser work** → worker that can automate or inspect the web UI
- **OS / SSH / Docker work** → worker closest to the target machine or shell
- **Writing / summary** → worker with strong language output

## Model-per-agent routing

Assign models per worker rather than using one global model.

Suggested pattern:
- master/planner → strongest general model you can afford
- coding worker → strongest code model you can afford
- execution worker → faster/cheaper model, because tools do most of the work
- writing worker → strong language model
- research worker → cost-effective model with good synthesis

The point is to match the model to the job, not to maximize raw model quality everywhere.

## Telegram / terminal / dashboard usage

- **Telegram**: use as the mobile/front-door channel when the user is away from the computer
- **cmux / terminal**: use for parallel local execution and direct control
- **Dashboard / Kanban**: use for task overview, management, and handoff tracking

These are user interaction modes, not separate layers of authority.

## Intake template

When the user gives the master agent a task, capture:
- what needs to be done
- the desired result
- any constraints
- the required output format

A simple prompt template:

- Help me do [task].
- The goal is [result].
- Constraints: [time / tools / format / scope].
- If needed, split it into subtasks and assign them to the right workers.
- Return a final answer I can use directly.

## Pitfalls

- Do not treat worker names as roles. A worker is an execution instance; a role is a capability.
- Do not require every worker to be in the Telegram group. The master can be the only user-facing endpoint.
- Do not assume the dispatcher can spawn every assignee. The assigned profile must exist on disk and be spawnable.
- Treat `running` / `stopped` as gateway state, not a binary usable/unusable flag. A `stopped` profile can still be invoked on demand with `hermes -p <profile> chat -q "..."`.
- Do not use Kanban as a knowledge store. It is for task flow.
- Do not over-split the system too early. Start with a small registry and expand only when a bottleneck appears.

## Practical first version

A good first version is:
- one master agent
- one coding worker
- one Windows/WSL worker
- one registry file
- one Kanban board
- one consistent model policy

That is usually enough to start getting the benefits of orchestration without adding unnecessary complexity.

Session-derived routing notes are captured below in the profile / wrapper routing section.

## Profile / wrapper routing

When a user wants one machine to call a worker profile on another machine:

- Verify the remote profile actually exists on the remote host.
- Treat profile names, wrapper commands, and sticky defaults as separate layers.
- Do not rely on renaming `default`; if a new stable entry is needed, create a cloned profile and keep the original root profile intact.
- If a dedicated remote worker already exists for the target host, prefer that worker chain over direct SSH. Use direct SSH only as the fallback path or for one-off diagnostics.

## Session-derived pitfalls to remember

- Do not treat a worker name as a role.
- Do not assume a conceptual assignee is spawnable.
- Before relying on dispatch, verify real profiles with `hermes profile list` and `hermes kanban assignees`.
- For thread hygiene, prefer `/new` for distinct topics, `/branch` for a preserved fork, `/queue` for same-topic follow-up, and `/steer` for light adjustments.
- Title important threads before splitting so they are easy to resume later.

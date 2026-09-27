---
name: hermes-multi-agent-orchestration
description: Design and operate Hermes-style multi-agent systems with a single coordinator, a worker registry, role-vs-node separation, and channel-specific interaction modes.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [multi-agent, orchestration, routing, worker-registry, coordinator, execution-nodes, telegram, cmux]
    related_skills: [hermes-agent, cross-agent-memory, subagent-driven-development, kanban-orchestrator, kanban-worker]
---

# Hermes Multi-Agent Orchestration

Use this skill when designing, explaining, or operating a system where one primary Hermes coordinates multiple worker agents across different machines, profiles, or interaction surfaces.

## What this skill is for

- Designing a single-coordinator multi-agent architecture
- Separating task roles from execution nodes
- Building a worker registry / routing table
- Deciding which tasks belong to which worker or environment
- Clarifying how Telegram, cmux, and desktop Hermes relate to each other
- Avoiding “multiple brains” fragmentation

## Core mental model

There are two different dimensions:

1. **Role layer** — what kind of work needs doing
   - Planner
   - Researcher
   - Engineer
   - Navigator
   - Writer
   - Operator

2. **Execution layer** — where the work runs
   - Mac Hermes
   - Win11 Hermes
   - WSL Hermes
   - wukong
   - other profiles / machines / sessions

Do not collapse these into one axis. A worker node can carry multiple roles over time, and a role can be routed to different nodes depending on environment, availability, and load.

## Default architecture

- **Primary Hermes**: the only conversational entry point and coordinator
- **Workers**: specialized agents or instances that execute routed tasks
- **Registry**: a human- or file-backed mapping of worker name → capabilities → entry command → return format
- **Shared memory**: one common long-term memory layer, not one per worker

The coordinator should:
- split work into lanes
- assign work to the right worker
- keep the user-facing conversation simple
- merge and summarize results

Workers should:
- execute one bounded assignment at a time
- return a predictable summary
- avoid acting as independent user-facing brains unless explicitly desired

## Recommended interaction modes

Treat user-facing interfaces as modes, not hierarchy:

- **Telegram**: mobile / away-from-desk interaction
- **cmux**: execution / parallel command-line work
- **Desktop Hermes**: management / overview / task triage

These modes can all connect to the same multi-agent system, but they serve different human workflows.

## Worker registry fields

At minimum, keep these fields for each worker:

- name
- role(s)
- host / machine
- profile / instance name
- capabilities
- entry command
- return format
- status / availability
- notes / constraints

In practice, many setups keep this registry in Obsidian as a synced routing layer. A good pattern is:
- one full template note
- one compact quick-routing note
- one usage-rules note
- one landing-index note for active roles

## Routing flow

1. User sends task to the primary Hermes.
2. Hermes identifies the task role(s).
3. Hermes checks the worker registry.
4. Hermes chooses a worker node based on capability + environment + availability.
5. Hermes sends the task through the correct channel.
6. Worker returns a structured result.
7. Hermes summarizes and responds to the user.

## Common routing heuristics

- Code / debugging → Engineer-capable worker
- Linux / Docker / SSH / server tasks → Operator-capable worker
- Windows-specific work → Win11 worker
- Long-running background work → stable always-on node
- Web interaction / browser ops → Navigator-capable worker
- Writing / summarizing → Writer-capable worker
- Research / reading / synthesis → Researcher-capable worker

## Important design rules

- Keep the user talking to one main agent whenever possible.
- Do not make every worker a direct chat endpoint unless you explicitly want a noisy, multi-voice system.
- Prefer a stable always-on Windows desktop node for long-running and heavy work when that is the hardware advantage.
- Let the coordinator own decomposition, scheduling, and final synthesis.
- Let workers own execution.
- Keep role definitions and machine definitions separate.

## Anti-patterns

- Turning every worker into a separate “brain” the user must remember
- Putting role names and machine names in the same bucket
- Forcing all workers into the same chat surface
- Making the coordinator do execution work instead of coordination
- Over-optimizing for abstraction before the registry and routing rules are stable

## OfficeCLI-backed document workers

When workers create or modify `.docx`, `.xlsx`, or `.pptx` through OfficeCLI, use the staged artifact contract, one-writer-per-file rule, and validate/issues/text/screenshot delivery gate in `references/officecli-document-workers.md`. Treat the coordinator's independent verification—not the worker's claimed output—as completion proof. OfficeCLI's MCP is a single generic `officecli(command)` tool, so MCP tool filtering cannot enforce verb-level or path-level isolation; use a wrapper when strict command or root restrictions are required.

## Document-generation orchestration

For multi-agent work that must produce or modify Word/PDF deliverables (especially tender documents):

1. Inspect the source tender, technical specification, and existing target documents before dispatching workers.
2. Build a compact factual brief containing project facts, quantities, deadlines, standards, unknowns, and explicit no-fabrication boundaries.
3. Dispatch independent workers in parallel with different writing roles or styles, while keeping factual requirements identical.
4. Stage each worker's draft in a temporary file or structured result first; do not let workers overwrite the final deliverables directly.
5. Have the coordinator review for omissions, contradictions, unsupported claims, and alignment with the target document's own section numbering.
6. Back up each target document before insertion, then merge the approved draft into the correct section.
7. Re-open/extract the resulting documents and verify headings, section coverage, file readability, and formatting before reporting success.
8. If the terminal/security layer requests approval to launch independent profiles or write files, stop and obtain that approval rather than claiming the work completed.

For tender work, preserve deliberate model diversity in wording and organization, but never create factual contradictions between versions. Treat model identity, provider, and authentication state as separate fields; a worker profile can be healthy while its configured default credential is not.

**Dispatch timing note**: launching workers via `hermes -p <profile> chat -q ... -Q` may trigger Hermes's own security scanner for spawning independent profiles, which blocks the command until the user approves it. Anticipate this: after dispatching parallel background workers, immediately verify each output file exists (`wc -l /tmp/worker_output.md`) rather than assuming they completed. If a file is empty or missing, the security layer blocked it — inform the user, do not retry silently.

**Timeout note**: large content-generation tasks (300+ lines of structured Chinese text) can exceed the default 180s timeout. Either:
- Increase `timeout=600` on the terminal tool, or
- Use `background=true + notify_on_complete=true`.
The `delegate_task` tool is less suitable here because child agents cannot read temporary files from the coordinator's workdir by default.

## Practical starting point

When first adopting this architecture:

1. Choose one primary Hermes as the only entry point.
2. Identify a small set of core roles.
3. List actual worker nodes in a registry.
4. Route tasks from the primary Hermes to those nodes.
5. Keep the registry simple until the routing patterns stabilize.

## When to load references

Load the supporting reference when you want the concrete, session-specific mapping of roles, modes, and worker nodes used in the current design discussion.

- `references/hermes-multi-agent-routing-notes.md` — session-specific worker routing notes, including SSH invocation patterns and the Win11 `winner` wrapper

# Hermes Multi-Agent Routing Notes

Session-derived notes for the Hermes multi-agent orchestration skill.

## User’s current design intent

- One primary Hermes should be the only conversational entry point.
- Sub-agents should mostly act as backend workers, not direct chat endpoints.
- Role definitions and machine definitions must stay separate.
- The user cares about stable long-running execution on the Win11 desktop.
- The user wants the Win11 machine to absorb load and survive laptop sleep / carry-around workflows.

## Current role layer discussed

- Hermes: coordinator / planner / router / synthesizer
- Researcher: search, reading, technical investigation
- Engineer: coding, debugging, refactoring, scripting
- Navigator: browser automation and web interaction
- Writer: documentation, summaries, prompts, emails
- Operator: Linux / WSL / Windows / SSH / Docker / server operations

## Current execution nodes discussed

- Mac Hermes: primary coordinator and main interaction surface
- wukong: coding-oriented worker on Mac
- Win11 Hermes: stable desktop execution node for heavier or long-running tasks
- WSL Hermes: Linux/WSL execution node when that environment is the right place to run work

## Interaction modes

- Telegram: mobile / away-from-desk task exchange
- cmux: execution mode for parallel terminal and agent work
- Desktop Hermes: overview / triage / organization mode

## Routing principle

The coordinator should first decide the task role, then choose the best execution node for that role based on environment and availability.

## Win11 worker invocation pattern (session-derived)

A concrete worker profile can live on the Win11 machine and be exposed through a local wrapper alias, while the Mac-side coordinator calls it over SSH.

### Observed mapping

- Mac wrapper: `/Users/liangzhu/bin/call-winner`
- SSH target: `zl@192.168.26.62`
- Win11 profile: `winner`
- Win11 alias wrapper: `C:\Users\zl\.local\bin\winner.bat`

### Observed call chain

1. Mac-side coordinator invokes `/Users/liangzhu/bin/call-winner`
2. The wrapper SSHes to `zl@192.168.26.62`
3. Windows wrapper `winner.bat` forwards to `hermes -p winner`
4. Hermes on Win11 runs the task in the `winner` profile

### Validation pattern

Use a very small prompt first to verify the end-to-end route:

```bash
/Users/liangzhu/bin/call-winner "只回复 OK"
```

If the remote shell needs Windows-style quoting, pass the message as one quoted string in the SSH command.

## What not to do

- Do not treat Win11 Hermes and WSL Hermes as new abstract roles.
- Do not force the user to talk to every worker directly.
- Do not merge all channels into one undifferentiated interface.
- Do not lose the original hardware rationale for the Win11 node.

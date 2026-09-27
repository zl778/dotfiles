---
name: herdr-terminal-multiplexer
description: "Use for Herdr pane, split, scroll, Agent, and remote issues."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [herdr, terminal, multiplexer, panes, tmux, agent-runtime, troubleshooting]
    category: software-development
---

# Herdr terminal multiplexer

Use this skill when the user asks about Herdr (`herdr.dev`), especially pane splitting, keyboard behavior, scrollback, Agent/TUI display, Agent automation, remote attach, or release changes.

## Source-of-truth order

1. Prefer the official Herdr documentation at `https://herdr.dev/docs/` for current behavior and keybindings.
2. Use the canonical GitHub repository and release notes at `https://github.com/ogulcancelik/herdr` for implementation details, regressions, and version-specific fixes.
3. Treat search snippets and third-party articles only as discovery aids; verify important claims against the official docs or GitHub API/release pages.
4. Always identify the Herdr version, host OS, terminal emulator, and pane application when diagnosing behavior.

## Explain the architecture before giving a workaround

Make the distinction clear:

- Terminal.app/Ghostty native splits are separate terminal views with local scrollback behavior.
- Herdr splits are panes managed by a terminal multiplexer/server. The pane is a PTY-backed session, and Herdr owns focus, layout, input routing, and viewport behavior.
- A pane running Claude Code, Codex, OpenCode, vim, htop, or another full-screen TUI may use the terminal alternate screen. Its visible screen and scrollback are not equivalent to a plain shell's normal scrollback.

Do not state that a Herdr pane's scroll is independent merely because the panes are visually separated. Verify whether the user is in normal mode or copy mode and whether the foreground application uses alternate-screen behavior.

## Diagnose split-and-scroll reports

1. Ask or infer the exact split command (`Cmd+D`, Herdr prefix command, or terminal-emulator command).
2. Identify whether the user is scrolling with a mouse/trackpad, keyboard, or pane application's own UI.
3. Identify which pane is focused and whether the behavior changes after selecting the pane.
4. Test Herdr copy mode instead of assuming normal-mode wheel scrolling is Herdr scrollback:
   - default prefix is `Ctrl+B`;
   - press `Ctrl+B`, release it, then press `[`;
   - use `PageUp`, `PageDown`, `Ctrl+U`, `Ctrl+D`, arrows, or `h/j/k/l`;
   - exit with `Esc` or `q`.
5. If copy mode works, explain that normal-mode wheel events may be routed to the foreground application or live viewport rather than acting like Terminal.app's native local scroll.
6. If copy mode also moves with live output, record the reproduction as a possible viewport/copy-mode issue; Herdr issue #680 describes copy-mode or mouse-scroll views continuing to advance while output is being written.
7. If the pane is a full-screen TUI and history is missing, check alternate-screen limitations. Herdr issue #1304 documents the lack of full normal scrollback for alt-screen TUI panes; do not promise Terminal.app/tmux-equivalent history without verification.

## Version-aware reporting

When summarizing a release:

- obtain the latest release from the canonical GitHub releases/API page;
- report tag and publication date;
- separate Breaking Changes, Added, Changed, and Fixed;
- prioritize changes relevant to the user's workflow: Agent CLI facade, `agent wait`, `agent send-keys`, Agent view filtering/sorting, lifecycle state detection, remote attach, and platform support;
- clearly mark limitations and unresolved issues instead of presenting them as solved.

## Evidence and wording rules

Use calibrated language for behavior not directly reproduced: “通常意味着”“可能是”“需要用版本和前台程序复现”。 Do not claim that Herdr's panes literally share one scroll buffer unless the evidence demonstrates that; distinguish shared client view state, pane-local viewport, foreground-app mouse handling, and alternate-screen behavior.

For a useful answer, give:

- conclusion first;
- the architecture difference in plain language;
- a concrete test/workaround;
- a limitation or issue link when relevant;
- the exact command/key sequence and what result should be expected.

## Reference material

See `references/herdr-scrollback-and-splits.md` for the verified notes and links gathered from the official docs and canonical issue tracker.

# Hermes multi-agent routing notes

This reference captures the session pattern for landing worker roles into a reusable registry.

## Current role set

- researcher
- engineer
- navigator
- operator
- writer

## Current routing pattern

- researcher → research, reading, source checking, synthesis
- engineer → coding, debugging, refactoring, testing
- navigator → browser actions, login, downloads, page verification
- operator → terminal, SSH, WSL, Docker, system ops
- writer → documentation, email, Markdown, rewriting

## Current note layout in Obsidian

- Full template: `Hermes-worker通讯录模板.md`
- Compact registry: `Hermes-worker通讯录精简版.md`
- Usage rules: `主Hermes读取worker通讯录的使用规范.md`
- Landing index: `Hermes-worker角色落地清单.md`

## Why this pattern works

- Main Hermes stays the only primary entry point.
- Worker identity is separated from execution surface.
- Routing rules are readable and editable outside the code path.
- Future roles can be added without changing the dispatch mental model.

## Practical checklist for adding a role

1. Create the profile.
2. Write a role-specific SOUL.md.
3. Set the role-appropriate model.
4. Update the Obsidian registry notes.
5. Add the role to the landing index.
6. Verify the profile appears in `hermes profile list`.

## Session-specific routing examples

- Research /查证 /阅读 → researcher
- 编码 /调试 /改造 → engineer or wukong
- 网页 /登录 /下载 /验证 → navigator
- 系统 /终端 /WSL /Docker /SSH → operator
- 文档 /邮件 /Markdown /改写 → writer
---
title: Hermes Worker 通讯录精简版
aliases:
  - Worker 通讯录精简版
  - Hermes worker 精简通讯录
created: 2026-07-08
updated: 2026-07-08
type: guide
tags:
  - r/tools/hermes
---

# Hermes Worker 通讯录精简版

这是一份给主 Agent Hermes 直接读取的精简通讯录。

## 规则

- 主 Hermes 只看这份表，就能决定把任务交给谁。
- 只保留最关键字段：名称、角色、能力、入口、回传。
- 需要更详细说明时，再看完整版笔记。

## 精简 YAML

```yaml
workers:
  wukong:
    role: engineer
    capabilities: [coding, debugging, refactor, scripts]
    entry: hermes --profile wukong chat -q
    return_format: summary_plus_code_changes

  win11_hermes:
    role: operator
    capabilities: [windows, wsl, ssh, docker, system_ops]
    entry: ssh win11 "wsl hermes chat -q"
    return_format: standard_summary

  wsl_hermes:
    role: operator
    capabilities: [linux, docker, shell, deployment, scripts]
    entry: ssh win11 "wsl hermes chat -q"
    return_format: standard_summary

  winner:
    role: operator
    capabilities: [windows, wsl, ssh, docker, system_ops]
    entry: /Users/liangzhu/bin/call-winner
    return_format: standard_summary

  researcher:
    role: researcher
    capabilities: [search, read, summarize, compare, source_check]
    entry: researcher
    return_format: reliable_sources_plus_summary

  engineer:
    role: engineer
    capabilities: [coding, debugging, refactor, scripts, testing]
    entry: engineer
    return_format: code_changes_plus_test_results

  navigator:
    role: navigator
    capabilities: [browser, login, download, verify_pages]
    entry: navigator
    return_format: page_state_plus_result

  operator:
    role: operator
    capabilities: [terminal, ssh, wsl, docker, system_ops]
    entry: operator
    return_format: command_result_plus_status

  writer:
    role: writer
    capabilities: [documentation, email, markdown, summarize, rewrite]
    entry: writer
    return_format: polished_text_plus_outline
```

## 路由规则

- 编码 / 调试 → wukong
- Windows / WSL / Docker / SSH → Win11 Hermes 或 WSL Hermes
- 复杂任务 → 先由 Hermes 拆解，再分派

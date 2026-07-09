---
title: Hermes Worker 通讯录模板
aliases:
  - Worker 通讯录模板
  - Hermes worker 通讯录
created: 2026-07-08
updated: 2026-07-08
type: guide
tags:
  - r/tools/hermes
---

# Hermes Worker 通讯录模板

这份笔记用于让主 Agent Hermes 认识并调用各个 worker。

主 Hermes 不需要记住所有实现细节，只需要知道：
1. 这个 worker 叫什么
2. 它擅长什么
3. 怎么把任务交给它
4. 它完成后怎么回传

## 一、表格版

| 名称           | 角色                  | 所在位置                | 主要能力                        | 调用方式                     | 回传方式            |
| ------------ | ------------------- | ------------------- | --------------------------- | ------------------------ | --------------- |
| wukong       | Engineer            | Mac 本机 / 独立 profile | 编码、调试、重构、脚本开发               | cmux / 本地 Hermes profile | 标准总结文本 + 代码变更摘要 |
| Win11 Hermes | Operator / Engineer | Win11 机器            | Windows、WSL、SSH、Docker、系统操作 | SSH / 本地命令 / Telegram 入口 | 标准总结文本          |
| WSL Hermes | Operator / Engineer | Win11 下的 WSL | Linux、Docker、shell、部署、脚本 | SSH / 本地命令 / Telegram 入口 | 标准总结文本 |
| winner | Operator / Engineer | Win11 机器（SSH: zl@192.168.26.62） | Windows、WSL、SSH、Docker、系统操作 | `/Users/liangzhu/bin/call-winner` / SSH / Kanban | 标准总结文本 |
| researcher | Researcher | Mac / 独立 profile | 资料搜索、阅读、筛选、研究整理 | `researcher` / `hermes -p researcher chat -q` | 可靠来源 + 结构化总结 |
| engineer | Engineer | Mac / 独立 profile | 编码、调试、重构、脚本实现 | `engineer` / `hermes -p engineer chat -q` | 代码变更摘要 + 测试结果 |
| navigator | Navigator | Mac / 独立 profile | 浏览器操作、点击、登录、下载、网页验证 | `navigator` / `hermes -p navigator chat -q` | 页面状态 + 结果摘要 |
| operator | Operator | Mac / 独立 profile | 系统、终端、WSL、SSH、Docker、运维 | `operator` / `hermes -p operator chat -q` | 命令结果 + 状态摘要 |
| writer | Writer | Mac / 独立 profile | 文档、邮件、Markdown、总结、改写 | `writer` / `hermes -p writer chat -q` | 整理后的正文 + 结构化摘要 |

## 二、扩展版字段

如果以后要继续扩展，可给每个 worker 再补这些字段：

- 固定名称
- 机器 / 设备
- profile 名称
- 负责角色
- 适合任务
- 不适合任务
- 入口命令
- 结果回传格式
- 当前状态（空闲 / 忙碌 / 不可用）
- 备注

## 三、YAML 版模板

```yaml
workers:
  wukong:
    name: wukong
    role: engineer
    host: mac
    profile: wukong
    entry: hermes --profile wukong chat -q
    capabilities:
      - coding
      - debugging
      - refactor
      - script-development
    unsuitable_for:
      - browser-automation
      - long-form-research
    return_format: standard_summary_plus_code_changes
    status: idle
    notes: Mac 上的编码副手

  win11_hermes:
    name: Win11 Hermes
    role: operator
    host: win11
    profile: winner
    entry: /Users/liangzhu/bin/call-winner
    capabilities:
      - windows
      - wsl
      - ssh
      - docker
      - system-operations
    unsuitable_for:
      - mac-only-operations
      - browser-only-workflows
    return_format: standard_summary
    status: idle
    notes: Windows / WSL 执行节点

  wsl_hermes:
    name: WSL Hermes
    role: operator
    host: win11-wsl
    profile: default
    entry: ssh win11 "wsl hermes chat -q"
    capabilities:
      - linux
      - docker
      - shell
      - deployment
      - scripts
    unsuitable_for:
      - mac-only-operations
      - browser-only-workflows
    return_format: standard_summary
    status: idle
    notes: Linux / WSL 执行节点

  researcher:
    name: researcher
    role: researcher
    host: mac
    profile: researcher
    entry: researcher
    capabilities:
      - search
      - read
      - summarize
      - compare
      - source-check
    unsuitable_for:
      - direct-system-ops
      - browser-only-workflows
    return_format: reliable_sources_plus_summary
    status: idle
    notes: 资料搜索与研究整理

  engineer:
    name: engineer
    role: engineer
    host: mac
    profile: engineer
    entry: engineer
    capabilities:
      - coding
      - debugging
      - refactor
      - script-development
      - testing
    unsuitable_for:
      - browser-only-workflows
    return_format: code_changes_plus_test_results
    status: idle
    notes: 编码与调试副手

  navigator:
    name: navigator
    role: navigator
    host: mac
    profile: navigator
    entry: navigator
    capabilities:
      - browser-automation
      - login
      - download
      - page-verification
    unsuitable_for:
      - direct-system-ops
      - code-only-workflows
    return_format: page_state_plus_result
    status: idle
    notes: 浏览器与网页执行节点

  operator:
    name: operator
    role: operator
    host: mac
    profile: operator
    entry: operator
    capabilities:
      - terminal
      - ssh
      - wsl
      - docker
      - system-ops
    unsuitable_for:
      - browser-only-workflows
    return_format: command_result_plus_status
    status: idle
    notes: 系统与运维执行节点

  writer:
    name: writer
    role: writer
    host: mac
    profile: writer
    entry: writer
    capabilities:
      - documentation
      - email
      - markdown
      - summarization
      - rewriting
    unsuitable_for:
      - direct-system-ops
      - browser-only-workflows
    return_format: polished_text_plus_outline
    status: idle
    notes: 文档整理与改写节点
```

## 四、主 Hermes 的调用规则

1. 任务先交给主 Hermes。
2. 主 Hermes 判断任务类型。
3. 主 Hermes 查通讯录。
4. 选择最合适的 worker。
5. 通过对应入口发任务。
6. worker 完成后回传结果。
7. 主 Hermes 汇总后再给用户。

## 五、最简单的路由规则

- 编码 / 调试 → wukong
- Windows / WSL / Docker / SSH → Win11 Hermes 或 WSL Hermes
- 复杂任务先拆解，再分派

## 六、后续可以补充的 worker

这 5 个角色已经落地：

- Researcher
- Engineer
- Navigator
- Operator
- Writer

如果以后还要继续扩展，可以再加：

- Reviewer
- Tester
- Archivist

只要保持同样字段，主 Hermes 就能统一调度。

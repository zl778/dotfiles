---
title: Win11 winner 调用说明
aliases:
  - winner 调用说明
  - Mac 调用 Win11 winner
created: 2026-07-09
updated: 2026-07-09
type: guide
tags:
  - r/tools/hermes
  - r/tools/win11
---

# Win11 winner 调用说明

这份笔记说明 Mac 上的 default 如何调用 Win11 机器上的 `winner` profile。

## 一、前提条件

- Mac 可以通过 SSH 连接 Win11
- Win11 上已存在并启动 `winner` profile
- `call-winner` 脚本已创建并放入 `~/bin/`

## 二、调用方式

```bash
call-winner "任务内容"
```

脚本内部实际执行：

```bash
ssh zl@192.168.26.62 "winner chat -q \"<任务内容>\""
```

## 三、最小测试

建议先测试一个很短的任务，例如：

```bash
call-winner "只回复 OK"
```

## 四、文件位置

- 脚本：`/Users/liangzhu/bin/call-winner`
- Worker 通讯录完整版：`/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-worker通讯录模板.md`
- Worker 通讯录精简版：`/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-worker通讯录精简版.md`
- Win11 侧别名脚本：`C:\Users\zl\.local\bin\winner.bat`

---
title: 主 Hermes 读取 Worker 通讯录的使用规范
aliases:
  - 主Hermes读取worker通讯录的使用规范
  - Worker 通讯录读取规范
created: 2026-07-08
updated: 2026-07-08
type: guide
tags:
  - r/tools/hermes
---

# 主 Hermes 读取 Worker 通讯录的使用规范

这份规范用于让主 Agent Hermes 知道：先读哪份通讯录、什么时候看完整版、什么时候只看精简版。

## 一、默认读取顺序

1. 先读精简版
路径：
/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-worker通讯录精简版.md

用途：
- 快速判断任务该派给谁
- 日常路由时优先使用

2. 需要更细时，再读完整版
路径：
/Users/liangzhu/Library/Mobile Documents/iCloud~md~obsidian/Documents/PKM/30_Resources/AI/Hermes-worker通讯录模板.md

用途：
- 新增 worker
- 修改 worker 职责
- 检查能力边界、回传格式、备注

## 二、什么时候只看精简版

以下情况主 Hermes 只看精简版就够了：

- 任务很明确
- 只需要快速路由
- 已经知道谁来做
- 不需要展开解释

例子：
- 编码 / 调试 → wukong 或 engineer
- 研究 / 查证 / 阅读 → researcher
- 网页操作 / 登录 / 下载 / 验证 → navigator
- 系统 / 终端 / WSL / Docker / SSH → operator、Win11 Hermes 或 WSL Hermes
- 文档 / 邮件 / Markdown / 改写 → writer

## 三、什么时候要看完整版

以下情况主 Hermes 应该切到完整版：

1. 新增 worker
例如：Researcher、Navigator、Writer、Reviewer。

2. 修改 worker 职责
例如：wukong 增加测试职责，Win11 Hermes 增加远程部署职责。

3. 任务边界不清
例如：任务该给 wukong 还是 WSL Hermes。

4. 需要统一规范输出格式
例如：所有 worker 都要按固定格式回传。

## 四、主 Hermes 决策流程

1. 先判断任务类型
2. 先查精简版通讯录
3. 选最合适 worker
4. 如果不确定，再查完整版
5. 分派任务
6. 收回结果
7. 汇总给用户

## 五、简化理解

- 精简版：用来“派单”
- 完整版：用来“管理和扩展”

## 六、使用原则

- 日常运行：先看精简版，够用就不翻完整版。
- 系统维护或扩展：先看完整版，再决定怎么改。

## 七、推荐习惯

把主 Hermes 当成一个会查通讯录的总调度：

- 快速任务：只看精简版
- 复杂任务：先看精简版定位，再看完整版确认

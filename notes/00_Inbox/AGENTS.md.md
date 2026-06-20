  项目规则

// 项目概况

- 项目名称：xxx

- 一句话描述：xxxx

- 技术栈：Python 3.11 + FastAPI + PostgreSQL + Redis

- 包管理：npm

// 代码规范

- 命名风格：Python 用 snake_case，JS/TS 用 camelCase

- 缩进：4 空格（Python），2 空格（JS/TS）

- 类型注解：Python 函数必须有类型注解

- 注释：中文注释，复杂逻辑要写为什么这么做

目录结构

- src/ — 主要代码

- tests/ — 测试文件，与 src 目录结构对应

- scripts/ — 工具脚本

- docs/ — 文档

工作流规则

- 修改前先读一遍现有代码理解结构

- 不允许修改 generated/、vendor/、.git/ 目录下的任何文件

- 每次提交前必须：lint 检查 → 测试通过

- 测试命令：pytest tests/ -x -v

- Lint 命令：ruff check src/

个人偏好

- 用中文回复

- 回答要简洁，不需要解释工具调用过程

- 主动指出代码中的潜在问题

常用命令

- 启动开发服务器：uvicorn src.main:app --reload

- 运行测试：pytest tests/ -x -v

- Lint 检查：ruff check src/

- 构建：poetry build
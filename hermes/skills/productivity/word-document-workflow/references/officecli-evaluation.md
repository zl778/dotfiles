# OfficeCLI 评估与 Hermes 接入参考

基于 2026-07-17 对 `https://github.com/iOfficeAI/OfficeCLI` 的仓库 README、`SKILL.md`、examples 和 Wiki 检查。

## 已确认能力

- 支持 `.docx`、`.xlsx`、`.pptx` 的创建、读取、修改。
- 单一自包含二进制，不要求安装 Microsoft Office、Python 或 Node.js 运行时。
- macOS Apple Silicon 可用；仓库提供 Homebrew、npm、安装脚本和 Release 二进制路径。
- DOM-like path：`create`、`view`、`get`、`query`、`set`、`add`、`remove`、`batch`、`dump`、`merge`、`validate`。
- `view html` / `view screenshot` / `watch` 支持渲染后检查；适合 Agent 的“读结构 → 修改 → 渲染 → 检查”闭环。
- resident mode 会缓存文件；OfficeCLI 自己的 `get/query/view/dump` 可看到最新编辑，交给 Python、Word、LibreOffice 或上传前必须 `save`/`close` 刷盘。
- 模板 `merge` 支持用 JSON 替换 `{{key}}`，适合批量项目变体。
- Excel 侧覆盖单元格、公式、工作表、排序、表格、图表、条件格式、数据验证、透视表、切片器、命名范围等；README 声称内置 350+ 公式函数，但必须用真实报价表复核。
- Word 侧覆盖段落、run、表格、页眉页脚、样式、目录、脚注、批注、水印、图片、域、编号等；复杂排版仍需实际 Word/LibreOffice 复核。
- Wiki 列出内置 MCP server；MCP 使用单一 `command` 字符串参数，例如 `{"command":"help docx paragraph"}`，不是假设的多字段结构化参数。

## 适合用户工作流的分层方案

```text
Supervisor/default：拆解、选择工具、审核、版本控制
worker/writer/wukong：执行文档任务
OfficeCLI：结构化读写、批处理、初步验证、渲染
Word/Excel/LibreOffice：最终兼容性与视觉抽查
```

首批验证对象应是：

1. 一份复制后的真实投标 `.docx` 模板；
2. 一份复制后的真实设备/报价 `.xlsx`；
3. 项目名称全局替换；
4. 页眉、页脚、表格和编号保持；
5. Excel 公式、合并单元格、排序和打印设置；
6. `validate` + HTML/PNG 渲染 + 重新读取关键字段。

## Hermes 任务合同模板

```text
任务类型：Office 文件修改
输入：/项目/投标文件-v1.docx
输出：/项目/投标文件-v2.docx
约束：不覆盖输入；OneDrive 文件先复制到临时目录或新版本
操作：明确列出 set/add/remove/merge 操作
验收：validate；输出存在；关键字段 read-back；渲染 HTML/截图；报告兼容性风险
```

## 不应过早做出的结论

- 不要仅凭空白文档或 README 宣称可完全替代 Word/Excel。
- 不要跳过实际 Word/Excel 打开检查，尤其是分页、字体、页眉页脚、目录页码、复杂表格、外部链接、OLE、宏和特殊模板。
- 不要让 Agent 直接覆盖正式投标文件；保留 `_v2`、`_v3` 版本和原始备份。
- 不要第一步就接 MCP；先用直接 CLI 调通、记录命令、固定输出验收合同，再决定是否需要 MCP。

## 安全检查

安装脚本会从网络下载二进制，且工具默认可能检查更新、安装 Agent Skill。正式用于投标文件前应检查：版本、下载来源/checksum、写入目录、更新开关，以及是否存在任何上传文件行为。

## 2026-07-18 文档研究补充

本次核验了仓库 README、中文 README、Wiki 首页、命令参考、安装、批处理、Raw XML、examples，以及 Word/Excel/PowerPoint reference：

- 核心格式是 `.docx`、`.xlsx`、`.pptx`；不要把可选插件的外部格式能力当成核心兼容性。
- 安装入口包括 macOS/Linux 安装脚本、Homebrew、npm、Windows PowerShell 脚本和 GitHub Releases；`officecli install [target]` 会复制自包含二进制、安装检测到的 Agent Skill，并为无 Skill 的工具注册 MCP。
- Word reference 明确列出段落、run、表格、页眉页脚、图片、文本框/形状、OLE、书签、脚注尾注、超链接、评论、目录、公式、样式、编号、内容控件、修订、图表和 Raw XML 等；形状/文本框的某些 `get` 结果仍是 raw preview，复杂分页必须实测。
- Excel reference 明确列出单元格、工作表、公式、表格、数据验证、评论、命名范围、图表、条件格式、筛选、Sparkline、Pivot Table、Slicer、OLE、排序、行列和分页符；文档声称内置 350+ 公式函数，但报价、外部链接、宏、Power Query/数据模型等不能仅凭函数数量推断为 Excel 等价。
- PowerPoint reference 列出幻灯片、占位符、形状、图片、表格、图表、主题、连接线、组合、媒体、公式、母版/布局、备注、评论、Zoom、3D、OLE、动画和 Mermaid 图；高级动画、母版、媒体和嵌入对象仍需 PowerPoint 复核。
- `batch` 当前 Wiki（v1.0.137+）说明默认原子回滚：所有项执行并出具失败报告，但任何失败会让目标文件保持批处理前状态；`--best-effort` 才保留成功项，`--stop-on-error` 控制早停。旧 README/Wiki 搜索摘要可能描述过“继续执行并保存成功项”，因此研究报告必须记录核验版本，不能混用旧语义。
- resident mode 的保存边界必须写入任务合同：OfficeCLI 自己的 `get/query/view/dump` 可见内存中的最新编辑，但交给 Python、Word、Excel、LibreOffice、渲染器或上传程序前必须 `save`/`close`。
- 版本和文档存在漂移风险：Wiki 页面正文仍有“Based on OfficeCLI v1.0.64”，而 Releases 页面显示 v1.0.138；引用能力时应同时记录页面版本/修订时间，并以目标 Release 的实际 CLI schema 为准。

## 对比结论

- OfficeCLI 的差异化在统一 CLI、DOM-like path、JSON/stdin batch、resident mode、HTML/PNG 预览和 MCP；它不是 Microsoft Word/Excel 排版和计算引擎的无条件替代品。
- `python-docx` 更适合可测试的 Python Word 业务逻辑，但没有内置分页渲染；`openpyxl` 更适合 Python Excel 数据处理，但官方文档明确“不会计算公式”，`data_only` 通常读取 Excel 上次保存的缓存值，Pivot Table 主要是读取/保留而非完整创建 API。
- LibreOffice 更适合 headless 转换、实际 Writer/Calc/Impress 打开与二次排版检查；它也有格式转换/兼容性变化风险，不能替代逐文件验收。
- 推荐投标工作流：OfficeCLI 负责 Agent 化的结构读取、窄范围修改、批处理和初步渲染；`python-docx`/`openpyxl` 负责复杂业务逻辑；LibreOffice 或 Microsoft Office 负责最终重算、分页、转换和视觉验收。

## 研究来源

- [OfficeCLI README_zh](https://github.com/iOfficeAI/OfficeCLI/blob/main/README_zh.md)
- [OfficeCLI Releases](https://github.com/iOfficeAI/OfficeCLI/releases)
- [Wiki Home](https://github.com/iOfficeAI/OfficeCLI/wiki)
- [Command Reference](https://github.com/iOfficeAI/OfficeCLI/wiki/command-reference)
- [Command Install](https://github.com/iOfficeAI/OfficeCLI/wiki/command-install)
- [Command Batch](https://github.com/iOfficeAI/OfficeCLI/wiki/command-batch)
- [Word Reference](https://github.com/iOfficeAI/OfficeCLI/wiki/word-reference)
- [Excel Reference](https://github.com/iOfficeAI/OfficeCLI/wiki/excel-reference)
- [PowerPoint Reference](https://github.com/iOfficeAI/OfficeCLI/wiki/powerpoint-reference)
- [Examples](https://github.com/iOfficeAI/OfficeCLI/wiki/examples)
- [Command Raw](https://github.com/iOfficeAI/OfficeCLI/wiki/command-raw)
- [Command MCP](https://github.com/iOfficeAI/OfficeCLI/wiki/command-mcp)
- [python-docx documentation](https://python-docx.readthedocs.io/)
- [openpyxl formula documentation](https://openpyxl.readthedocs.io/en/3.1/simple_formulae.html)
- [openpyxl Pivot Table documentation](https://openpyxl.readthedocs.io/en/stable/pivot.html)
- [LibreOffice command-line parameters](https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html)
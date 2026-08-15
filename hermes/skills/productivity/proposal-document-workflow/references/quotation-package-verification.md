# 多供应商报价文件验证清单

适用：根据询价函/招标文件 + 多供应商 XLSX 清单，生成多份 DOCX 报价文件。

## 1. 事实冻结

- 读取询价函 DOCX：项目名称、项目编号、采购单位、预算控制价、交货期、报价有效期、服务承诺、逐条技术要求。
- 读取 XLSX 全部供应商工作表：报价单位、品牌/型号、数量、单位、单价、金额公式、备注。
- 形成统一 brief；每个 worker 只接收同一份事实 brief，输出路径必须互不相同。

## 2. 价格复核

对每个供应商同时保留三种结果：

1. 源表公式结果；
2. 逐项金额重新相加结果；
3. 含税总价与预算控制价比较结果。

发现公式漏行时，不要沿用错误公式或擅自改价。报价文件应写明“源表结果”和“按完整清单重算结果”，并标出超预算金额。例如，源表合计公式若遗漏跳线行，完整清单结果可能高于预算。

## 3. Worker 调度与认证恢复

- 使用用户指定的 profile（如 `hermes -p wukong`、`hermes -p writer`），不要用未命名的临时 worker 替代。
- 通过 `-q` 明确源文件和绝对输出路径；不要依赖 worker 当前目录。
- 默认 provider 认证失败时，保留原 profile，改用已验证的 provider/model 重试；交付说明中明确“profile 保留、provider/model 发生 fallback”，不要声称原模型身份未改变。
- worker 的最终文字、diff 或“已完成”不是证据；必须独立检查文件存在、大小、可读性和内容。

## 4. DOCX 内容审核

逐份检查：

- 项目编号、采购单位、报价单位、品牌和精确型号；
- 分项数量、单位、单价、金额、税费和总价；
- 安装、调试、培训、质保、响应时间等服务费用是否明确包含；
- 每条技术要求的响应状态；未由清单明确证明的参数用“待厂家书面确认”；
- 选配件（如冗余电源）、授权期限表述不一致、型号/容量描述冲突；
- 盖章签字栏、材料清单和报价有效期；
- `core_properties.author` 和 `last_modified_by` 不应暴露 `python-docx` 等制作工具。

## 5. OfficeCLI resident 缓存与 schema

OfficeCLI 会为文件启动 resident。文件被其他程序修改后，先执行：

```bash
officecli close "文件.docx"
officecli validate "文件.docx"
```

否则 validate 可能读取修改前的内存版本。`python-docx` 自定义表格底色若产生严格 schema 错误（常见为 `w:shd` 缺少 `val` 或顺序不合法），先在 `/tmp/` 留备份，再删除非必要的 shading XML 或用 schema-valid 的 shading 重新生成；关闭 resident 后再次 validate。

## 6. 最终交付门槛

- 每份 DOCX 可由 `python-docx` 重新打开；
- 每份 `officecli validate` 通过；
- 关键事实和金额独立回读；
- 超预算或证据不足事项在文件中可见；
- 原询价函和原始清单不覆盖；修复文件使用新版本或在新生成文件上处理。

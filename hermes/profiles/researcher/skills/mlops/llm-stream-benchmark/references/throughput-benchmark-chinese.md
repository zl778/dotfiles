# 吞吐量基准测试（中文版）

此文件包含了从 `llm-throughput-benchmarking` 技能合并而来的中文内容。用于评估 Hermes 已配置 LLM provider 中，各模型的生成吞吐速度（token 生成吞吐与首 token 延迟）。

## 前置发现

在运行评测前，先发现当前可用的 provider 与凭证入口：

1. `hermes status` — 查看已登录 provider、API key 状态
2. `hermes auth list` — 查看 credential pool 中有哪些 provider
3. 读取环境变量或 Hermes credential store：
   - `~/.hermes/.env` 内可能存放 OpenAI/DeepSeek/NVIDIA 等 key
   - `~/.hermes/auth.json` 受保护，不可直接读取，但 `hermes` 子命令与其内部集成

## 标准化评测流程

1. **列出可用模型**
   - 对每个 provider，调用 `GET {base_url}/v1/models` 获取当前可用模型 ID
   - 只选择 Chat Completion 类模型（排除 embedding / safety 等专用模型）

2. **单次探针请求**
   - endpoint: `POST {base_url}/v1/chat/completions`
   - payload: `{"model": <id>, "messages": [{"role":"user","content":"Say ok"}], "max_tokens": 16}`
   - 使用 SSE 流式请求（`stream: true`），逐行读取 `data:` 事件

3. **度量采集**
   - **TTFT**：首段 `delta.content` 非空的时间差（相对于请求发出时刻）
   - **生成耗时**：请求发出到收到 `data: [DONE]` 的总 wall time
   - **吞吐 (tok/s)**：`usage.completion_tokens / 生成耗时`

## 坑点与约束

1. **Hermes 主链的 provider 与裸 API provider 并不完全等价**：某些 provider 在 CLI 里可用，但裸 `/v1/chat/completions` 可能返回 500 或不支持具体模型。
2. **TTFT 的 delta 位置**：如 Nous stepfun/step-3.7-flash:free，首段 token 常落在 `delta.reasoning` 或 `delta.reasoning_details[*].text`，`delta.content` 可能为空。评测时要同时监听 `content`、`reasoning`、`reasoning_details`，否则会误报 N/A。
3. **网络不稳定**：商用 API 有时会 SSL 异常 (SSLEOFError)，需重试或换上层库（requests / urllib）再验证，不要直接断定"该 provider 不可用"。
4. **不要用 Hermes UI 延迟度量**：Hermes 的 `streaming=false` 配置只控制前端显示，服务端仍接受 SSE；速度度量应在客户端通过 `usage.completion_tokens / 生成时段` 计算。
5. **成本意识**：`max_tokens=16` 的微型探测节省 token；比较阶段每个模型做 1~3 次。

## 输出格式

给出一张汇总表，至少包含：

- Provider
- Model
- TTFT (s)
- Tokens/s
- 错误/备注

以及结论：当前最快模型 + 推荐原因。

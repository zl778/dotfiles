# Nous 流式推理 API 性能报告

- 时间: 2026-06-01
- 模型: `stepfun/step-3.7-flash:free`
- 端点: Nous Inference API (`inference-api.nousresearch.com/v1`)
- 凭据来源: `~/.hermes/auth.json` => provider `nous`

## 方法

直接以 OpenAI Chat Completions SSE（`stream:true`）发起真实请求，并从服务端返回的 `chat.completion.chunk` 事件流中捕获 token 到达时刻。要点如下：

- 该模型首段 token 先进入 `delta.reasoning`，测量时按首个非空 `delta.content` 或 `delta.reasoning*` 事件作为首 token。
- 生成速度按 API 在流末尾返回的 `prompt_tokens`、`completion_tokens` 计算。

## 结果

- TTFT: 3613.74 ms
- 总延迟: 5250.20 ms
- 分片总数: 158
- 可见输出字符 (`delta.content`): 0
- 推理/推理明细字符: 658

- prompt_tokens (API): 25
- completion_tokens (API): 200

## 速度

- 首 token 后速度: 122.22 tok/s
- 整段平均速度: 38.09 tok/s

- TTFT 占总延迟: 68.8%

## 观察

- 该模型首段 token 先落在 `reasoning` 分支，说明这是带 thinking/reasoning 的响应；你在普通聊天结果里看不到即时文本，是因为最终可见内容后续才拼出。
- 这说明瓶颈在首 token 侧，而不是生成本身。这里的推理速度其实是 122 tok/s，但预热占掉了 3.6 秒。

---

## 参数快照

| 参数 | 主备 |
|---|---|
| 模型 | `stepfun/step-3.7-flash:free` |
| 端点 | `https://inference-api.nousresearch.com/v1` |
| 请求 | OpenAI Chat Completions | `stream: true` |
| max_tokens | 200 |
| temperature | 0 |
| 测次 | 1 |
| prompt | `用50字左右解释 TTFT（Time to First Token）。` |

## 定量观测结果

| 指标 | 值 |
|---|---|
| TTFT | 3613.74 ms |
| 总延迟 | 5250.20 ms |
| 分片总数 | 158 |
| 可见输出字符 `delta.content` | 0 |
| 推理/推理明细字符 | 658 |
| prompt_tokens (API) | 25 |
| completion_tokens (API) | 200 |
| 首 token 后速度 | 122.22 tok/s |
| 整段平均速度 | 38.09 tok/s |
| TTFT 占总延迟 | 68.8% |

## 时序趋势跟踪

# DeepSeek 流式推理 API 性能报告

- 时间: 2026-06-01
- 模型: `deepseek-v4-flash`
- 端点: DeepSeek API (`api.deepseek.com/v1`)
- 凭据来源: `~/.hermes/.env` => `DEEPSEEK_API_KEY`

## 方法

同上。DeepSeek 的 `deepseek-v4-flash` 模型不返回 `reasoning` 字段，content 直接出现在 `delta.content`。

## 结果

- TTFT: 1461.56 ms
- 总延迟: 1745.05 ms
- 分片总数: 27
- 可见输出字符: 61
- prompt_tokens (API): 18
- completion_tokens (API): 78

## 速度

- 首 token 后速度: 275.14 tok/s
- 整段平均速度: 44.70 tok/s
- TTFT 占比: 83.8%

## 对比

| 指标 | Nous `stepfun/step-3.7-flash:free` | DeepSeek `deepseek-v4-flash` |
|---|---|---|
| TTFT | 3613.74 ms | 1461.56 ms |
| 总延迟 | 5250.20 ms | 1745.05 ms |
| 首 token 后速度 | 122.22 tok/s | 275.14 tok/s |
| 整段平均速度 | 38.09 tok/s | 44.70 tok/s |

DeepSeek 的 TTFT 远低于 Nous（2.5x 快），生成速度则接近 2.3x。但 DeepSeek 返回的 completion_tokens 较少（78 vs 200），可能与模型倾向输出简短回复有关。注意：两个测试的 prompt 不同（Nous 测试首 token 先落入 reasoning 分支）。

## 时序趋势跟踪

| 时间 | 模型 | TTFT | 总延迟 | prompt_tokens | completion_tokens | 首 token 后速度 (tok/s) | 整段速度 (tok/s) | 备注 |
|---|---|---|---|---|---|---|---|---|
| 2026-06-01 20:59 | stepfun/step-3.7-flash:free | 3613.74 ms | 5250.20 ms | 25 | 200 | 122.22 | 38.09 | 首 token 先落入 reasoning 分支 |
| 2026-06-01 21:09 | deepseek-v4-flash | 1461.56 ms | 1745.05 ms | 18 | 78 | 275.14 | 44.70 | 正常 content 流，未走 reasoning |

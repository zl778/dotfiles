# SiliconFlow 速记 — provider 口径与坑

采集时间：2026-07-07，来自 macOS Hermes 当前会话（NVIDIA 标注的 MiniMax-M3 实际不存在）。

## base_url

`https://api.siliconflow.cn/v1`

OpenAI 兼容 chat completions、`/v1/models` 列举、bearer token 鉴权。

## 发现 model ID 的正确方法

```bash
curl -s https://api.siliconflow.cn/v1/models \
  -H "Authorization: Bearer $SILICONFLOW_KEY" | jq '.data[].id'
```

**永远不要从模型宣传名直接拼 ID** — 大小写、空格、版本号都敏感。复制 `/v1/models` 返回里的精确字符串。

## 已知常驻模型 ID（2026-07 采到）

| Provider | 正确 ID | 常见拼错（会 400） |
|----------|--------|------------------|
| MiniMax | `MiniMaxAI/MiniMax-M2.5` | `minimaxai/minimax-m3`（不存在）/ `MiniMax/M2.5`（少 AI）/ `MiniMaxAI/M2.5`（少 MiniMax） |
| DeepSeek | `deepseek-ai/DeepSeek-V4-Pro`、`deepseek-ai/DeepSeek-V4-Flash` | `deepseek-chat`（旧名） |
| GLM | `Pro/zai-org/GLM-5.1`、`zai-org/GLM-4.5-Air` | 很多旧 GLM ID 已下架 |
| Kimi | `moonshotai/Kimi-K2.7-Code`、`Pro/moonshotai/Kimi-K2.6` | — |
| 智谱 GLM-Image | `zai-org/GLM-Image` | — |

> 注意 `Pro/` 前缀：有的是免费版，有的是付费 Pro 版。Pro 版通常更高并发、付费计费。具体见硅基流动定价页。

## MiniMax-M2.5 实测数据（2026-07-07）

测试 prompt：54-token 中文短问，温度 0，max_tokens 200，跑 3 轮：

| 指标 | 第1轮 | 第2轮 | 第3轮 | 中位 |
|---|---:|---:|---:|---:|
| TTFT | 41385 ms | 10500 ms | 12675 ms | **12675 ms** |
| 总延迟 | 41833 ms | 10719 ms | 12880 ms | 12880 ms |
| 完成 tokens | 2197 | 521 | 637 | — |
| 整段 TPS | 52.5 tok/s | 48.6 tok/s | 49.5 tok/s | **~50 tok/s** |
| TTFT 占比 | 98.9% | 98.0% | 98.4% | ~98% |

**解读：**
- **TTFT 高得离谱但 TPS 正常** — 模型在内部做多版本推理 / 反思后才开始流式输出。不是网络问题，是模型特性。
- **输出里可见修订痕迹**（空行 + 第二段答案）— 内部重写到流式送达的中间态。
- **测量方式建议**：报告 TTFT 时仍按"首个非空 delta"算，但要在备注里说明模型有内部推理延迟。给用户体验估计时按 **12–15s 首字 + ~50 tok/s 出字** 算。

## 与 hermes config.yaml 配合的常见坑

用户 config 写的是 `minimaxai/minimax-m3`（小写、含 "i"），但这个 ID SiliconFlow 上不存在。三个解决路径：

1. **改 config**：把 `model.default` 改成 SiliconFlow 真实存在的 `MiniMaxAI/MiniMax-M2.5`，并把 `base_url` 设为 SiliconFlow。问题：和"当前 provider = nvidia"语义不一致。
2. **检查 NVIDIA 是否直连**：如果实际意图是走 NVIDIA NIM 直连 API，需要换一套 base_url + model id，**和 SiliconFlow 完全无关**。
3. **先验证再改**：用 curl 直接打 `https://integrate.api.NVIDIA.com/v1/chat/completions` 确认 MiniMax-M3 是不是真的在 NVIDIA 上可用。

完成后存回 Obsidian PKM `pages/` 目录的 `SiliconFlow 流式推理 API 性能报告.md`，追加一行到 `## 时序趋势跟踪` 表格里。

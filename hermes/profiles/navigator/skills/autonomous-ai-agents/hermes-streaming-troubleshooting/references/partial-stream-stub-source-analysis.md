# Partial-Stream-Stub Source Analysis

Extracted from Hermes source code (commit up to 2026-06-19).

## Where the Stub Is Built

**File:** `agent/chat_completion_helpers.py` — `interruptible_streaming_api_call()`

**Trigger:** The streaming generator raises an exception or ends cleanly without a finish_reason, AFTER some chunks were already delivered (`deltas_were_sent["yes"]` is True).

The stub is created at lines ~2610-2666:

```python
if result["error"] is not None:
    if deltas_were_sent["yes"]:
        # Re-raising would let the outer retry loop make the user wait.
        # Instead, return a partial response stub with finish_reason="length"
        # so the conversation loop's continuation machinery fires.
        # tool_calls=None prevents auto-execution of incomplete calls.
```

### Key behaviors:

1. **Text-only partial** (no tool calls dropped): returns stub with recovered text content + `finish_reason="length"`
2. **Mid-tool-call partial** (tool calls were being streamed): 
   - Sets `tool_calls = None` so incomplete tool calls never auto-execute
   - Appends user-visible warning: `"⚠ Stream stalled mid tool-call (write_file); the action was not executed. Ask me to retry if you want to continue."`
   - Stores dropped tool names in `response._dropped_tool_names`
   - Always uses `finish_reason="length"`

### Critical edge case: clean stream end mid-tool-call

When the provider closes the SSE stream cleanly (StopIteration, no exception, no finish_reason, no [DONE] signal — observed on NVIDIA Nemotron Ultra via the Nous dedicated endpoint), the code checks:

```python
_tool_args_dropped_no_finish = has_truncated_tool_args and finish_reason is None
if _tool_args_dropped_no_finish:
    logger.info("mid-tool-call stream drop, not an output-length truncation.")
```

It MUST route through the partial-stream-stub path (not finish_reason='length' from the provider), otherwise the user gets the misleading "Response truncated due to output length limit" error.

## Where the Stub Is Handled

**File:** `agent/conversation_loop.py` — `run_conversation()`

At lines ~1524-1666:

```python
if finish_reason == "length":
    if getattr(response, "id", "") == PARTIAL_STREAM_STUB_ID:
        agent._vprint(
            f"{agent.log_prefix}⚠️  Stream interrupted by network error "
            f"(finish_reason='length' on partial-stream-stub)",
            force=True,
        )
    else:
        agent._vprint(
            f"{agent.log_prefix}⚠️  Response truncated "
            f"(finish_reason='length') - model hit max output tokens",
            force=True,
        )
```

Then up to 3 continuation retries with specialized prompts (from `_get_continuation_prompt()`):

| Scenario | Continuation Prompt |
|----------|-------------------|
| Partial stub + dropped tool calls | "Your tool call (X) was too large and the stream timed out. Break content into multiple smaller tool calls (<~8K tokens each)." |
| Partial stub + text only | "The previous response was cut off by a network error mid-stream. Continue exactly where you left off." |
| Real length truncation | "Your previous response was truncated by the output length limit. Continue exactly where you left off." |

## Test Suite

**File:** `tests/run_agent/test_partial_stream_finish_reason.py`

- `TestPartialStreamStubFinishReason` — text-only and mid-tool-call stubs
- `TestCleanStreamEndMidToolCall` — clean stream end (StopIteration, no finish_reason, no [DONE])

## Constants

**File:** `hermes_constants.py`

```python
PARTIAL_STREAM_STUB_ID = "partial-stream-stub"
FINISH_REASON_LENGTH = "length"
```

## Key Issue References

- **#30963**: text-only partial streams had wrong finish_reason → caused loop to end the turn instead of continuing
- **#31998**: mid-tool-call partials needed to fire continuation machinery instead of ending immediately
- **#6600**: interrupt-requested handling during streaming (clean cancellation vs network error)

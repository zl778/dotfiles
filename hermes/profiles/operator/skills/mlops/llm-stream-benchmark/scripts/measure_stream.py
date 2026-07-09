#!/usr/bin/env python3
"""Reusable streaming latency/throughput benchmark for any OpenAI-compatible chat endpoint."""

import json
import sys
import time
import ssl
import urllib.request
import urllib.error
from pathlib import Path


def resolve_token(model_hint: str) -> str | None:
    """Resolve an API token from auth.json credential pool or .env file."""
    auth_path = Path.home() / ".hermes" / "auth.json"
    env_path = Path.home() / ".hermes" / ".env"

    # 1. auth.json credential pool
    if auth_path.exists():
        try:
            auth = json.loads(auth_path.read_text())
            # Check credential_pool first
            pool = auth.get("credential_pool", {})
            for provider_name, entries in pool.items():
                if isinstance(entries, list):
                    for entry in entries:
                        tok = entry.get("access_token") or ""
                        if tok and tok != "***":
                            return tok
            # Fallback: providers.<name>.access_token
            for provider_cfg in auth.get("providers", {}).values():
                if isinstance(provider_cfg, dict):
                    tok = provider_cfg.get("access_token") or ""
                    if tok and tok != "***":
                        return tok
        except Exception:
            pass

    # 2. .env file
    if env_path.exists():
        try:
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if "=" not in line or line.startswith("#"):
                    continue
                key, _, val = line.partition("=")
                val = val.strip("\"'")
                if val and val != "***":
                    return val
        except Exception:
            pass

    return None


def _ssl_context():
    """Create a verified SSL context using certifi (fixes macOS cert issues)."""
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return None


def main():
    if len(sys.argv) < 4:
        raise SystemExit(
            "usage: measure_stream.py <base_url> <model> <prompt> [max_tokens]\n\n"
            "Resolves API tokens from ~/.hermes/auth.json or ~/.hermes/.env. "
            "Pass --token <key> before <base_url> to override."
        )
    # Optional --token flag
    token = None
    idx = 1
    if len(sys.argv) > 2 and sys.argv[1] == "--token":
        token = sys.argv[2]
        idx = 3

    base_url = sys.argv[idx].rstrip("/")
    model = sys.argv[idx + 1]
    prompt = sys.argv[idx + 2]
    max_tokens = int(sys.argv[idx + 3]) if len(sys.argv) > idx + 3 else 200

    if not token:
        token = resolve_token(model)
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt or "hello"}
            ],
            "stream": True,
            "max_tokens": max_tokens,
            "temperature": 0,
            "stream_options": {"include_usage": True},
        }
    ).encode("utf-8")

    url = f"{base_url}/chat/completions"
    start = time.perf_counter()
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")

    chunks = 0
    content_chars = 0
    reasoning_chars = 0
    usage_prompt_tokens = None
    usage_completion_tokens = None
    ttft_ms = None
    first_content_ms = None

    try:
        ctx = _ssl_context()
        opener = urllib.request.urlopen if ctx is None else (
            lambda r, **kw: urllib.request.urlopen(r, context=ctx, **kw)
        )
        with opener(req, timeout=180) if ctx else urllib.request.urlopen(req, timeout=180) as resp:
            for raw_line in resp:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    ev = json.loads(data)
                except Exception:
                    continue
                now = time.perf_counter()
                choices = ev.get("choices") or []
                if choices:
                    delta = choices[0].get("delta") or {}
                    c = delta.get("content") or ""
                    if isinstance(c, str) and c:
                        chunks += 1
                        content_chars += len(c)
                        if first_content_ms is None:
                            first_content_ms = (now - start) * 1000
                    r = delta.get("reasoning") or ""
                    if isinstance(r, str) and r:
                        chunks += 1
                        reasoning_chars += len(r)
                        if first_content_ms is None:
                            first_content_ms = (now - start) * 1000
                    for rd in (delta.get("reasoning_details") or []):
                        if isinstance(rd, dict):
                            t = rd.get("text")
                            if isinstance(t, str) and t:
                                chunks += 1
                                reasoning_chars += len(t)
                                if first_content_ms is None:
                                    first_content_ms = (now - start) * 1000
                usage = ev.get("usage")
                if isinstance(usage, dict):
                    usage_prompt_tokens = usage.get(
                        "prompt_tokens", usage_prompt_tokens
                    )
                    usage_completion_tokens = usage.get(
                        "completion_tokens", usage_completion_tokens
                    )
        end = time.perf_counter()
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTPError {e.code}: {e.read().decode('utf-8', errors='replace')}")

    latency_ms = (end - start) * 1000
    ttft_ms = first_content_ms
    ttft2 = ttft_ms if ttft_ms is not None else None

    print("=== 测量结果 ===")
    print(f"TTFT:        {f'{ttft2:.2f} ms' if ttft2 is not None else 'N/A'}")
    print(f"总延迟:      {latency_ms:.2f} ms")
    print(f"分片总数:    {chunks}")
    print(f"可见字符:    {content_chars}")
    print(f"推理字符:    {reasoning_chars}")
    print(f"prompt_tokens(API): {usage_prompt_tokens}")
    print(f"completion_tokens(API): {usage_completion_tokens}")
    if ttft2 is not None and usage_completion_tokens:
        gen_ms = max(latency_ms - ttft2, 0)
        print(f"生成时段:    {gen_ms:.2f} ms")
        print(
            f"首 token 后速度: {usage_completion_tokens / (gen_ms / 1000):.2f} tok/s"
            if gen_ms
            else "首 token 后速度: N/A"
        )
        print(
            f"整段平均速度:   {usage_completion_tokens / (latency_ms / 1000):.2f} tok/s"
        )
        print(f"TTFT 占比:  {ttft2 / latency_ms * 100:.1f}%")


if __name__ == "__main__":
    main()

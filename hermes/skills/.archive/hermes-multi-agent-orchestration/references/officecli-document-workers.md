# OfficeCLI document workers: integration and acceptance notes

Use this reference when a Hermes coordinator routes DOCX/XLSX/PPTX work to workers or exposes OfficeCLI through CLI/MCP.

## OfficeCLI interface facts

The iOfficeAI/OfficeCLI repository provides a single binary for `.docx`, `.xlsx`, and `.pptx`, with DOM-like paths and commands including:

```text
help, load_skill, create, open, save, close,
view, get, query, validate, set, add, remove, move, swap,
batch, dump, raw, raw-set, mcp
```

Format aliases are `word -> docx`, `excel -> xlsx`, and `ppt/powerpoint -> pptx`. Prefer `officecli help <format> <element> --json` over guessing property names.

Resident-mode rule: OfficeCLI reads (`get/query/view/dump`) see its latest in-memory edits. Flush with `save` or `close` only before an external reader (python-docx/openpyxl/Word/renderer/upload) reads the file.

`batch` is atomic by default in recent versions: if any item fails, the batch rolls back. Use `--best-effort` only when partial application is explicitly desired.

## Coordinator/worker contract

A worker input should include:

```json
{
  "task_id": "office-...",
  "artifact_type": "docx|xlsx|pptx",
  "source_files": ["/workspace/input/source.docx"],
  "output_file": "/workspace/staging/worker-1.docx",
  "operation": "create|edit|review",
  "requirements": [],
  "constraints": {
    "no_overwrite_source": true,
    "allowed_root": "/workspace",
    "visual_check_required": true
  }
}
```

The worker must return a structured summary containing `success`, absolute artifact path, operation counts, warnings, and verification results. A worker's final message or claimed output path is not proof; the coordinator independently checks existence, size, content, and package validity.

Never allow multiple workers to modify the same Office file concurrently. Give each worker a unique staging copy and let the coordinator merge or promote only an independently verified artifact.

## Required delivery gate

Before reporting an Office artifact finished, run:

```bash
officecli validate "$OUTPUT"
officecli view "$OUTPUT" issues --json
officecli view "$OUTPUT" text --max-lines 1000
officecli view "$OUTPUT" screenshot -o /tmp/officecli-review.png
```

Also verify file existence, size, and checksum. Scan text for placeholders (`TODO`, `TBD`, `lorem ipsum`), empty required sections, and key requirement omissions. A passing `validate` alone is not delivery proof. If visual rendering is unavailable, report structural verification separately and do not claim visual verification.

## CLI versus MCP

OfficeCLI's built-in MCP server is started with:

```bash
officecli mcp
```

It communicates over stdio and exposes one tool named `officecli` with one parameter, `command`, which is a raw CLI command string or argv array. Hermes can configure it under `mcp_servers`:

```yaml
mcp_servers:
  officecli:
    command: "/absolute/path/to/officecli"
    args: ["mcp"]
    timeout: 300
    connect_timeout: 30
    tools:
      include: ["officecli"]
      prompts: false
      resources: false
```

Hermes registers the tool as `mcp_officecli_officecli` and reloads it with `/reload-mcp` or a fresh session. Because OfficeCLI MCP has one generic command tool, Hermes `tools.include` cannot restrict individual verbs such as `raw-set` or `remove`. For strict command/path isolation, use a wrapper that enforces an allowed root and verb whitelist before invoking OfficeCLI.

## Safety boundaries

- Keep source files read-only and write versioned siblings into `staging/` or `output/`.
- Keep Hermes approvals manual for document mutation; do not use global `--yolo` for this integration.
- Disable MCP prompts/resources and sampling unless specifically required.
- Treat `raw`, `raw-set`, plugins, deletion, and arbitrary paths as elevated operations.
- If an executable is missing, not on PATH, or not executable, record the setup blocker and fix installation/permissions; do not convert that transient state into a permanent capability refusal.
- Distinguish the iOfficeAI/OfficeCLI document-editing repository from similarly named natural-language Office generation projects before designing the integration.

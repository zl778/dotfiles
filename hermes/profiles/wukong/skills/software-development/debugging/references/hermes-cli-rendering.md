# Hermes CLI Rendering and ANSI Color Troubleshooting

Use this reference when a user asks why colored output, Markdown, boxes, status bars, or terminal styling in Hermes CLI/TUI does not look as expected.

## Quick diagnosis

1. Inspect the screenshot or terminal output first. Do not assume ANSI worked just because escape sequences were emitted.
2. Distinguish these layers:
   - Terminal capability: `TERM`, `COLORTERM`, truecolor/256-color support.
   - Hermes display settings: `display.skin`, `display.final_response_markdown`, `display.streaming`, `display.interface`.
   - Rich/Markdown rendering: final assistant responses may be stripped, rendered, or treated as raw ANSI.
   - Tool output sanitization: some tool paths intentionally strip ANSI before the model sees it.
3. Check the active profile config path with `hermes config path`, then inspect `display:` in that profile's config.

## Key setting: final_response_markdown

Hermes CLI final assistant content is controlled by:

```bash
hermes config set display.final_response_markdown raw
```

Modes:

- `strip`: removes Markdown syntax and presents plain text; ANSI color authored in the assistant response will not reliably render as intended.
- `render`: renders Markdown through Rich; good for prose/tables, but ANSI embedded in model text is not the primary path.
- `raw`: preserves ANSI escape sequences in final assistant content via Rich ANSI parsing; use when testing or intentionally emitting colored text.

Changing this config requires a fresh Hermes CLI session. Tell the user to exit and restart Hermes after setting it.

## Skin is not content color

`/skin` or `display.skin` changes Hermes chrome/theme: borders, titles, status bars, accents. It does not by itself make arbitrary assistant response text red/green/blue. If the user's goal is colored assistant content, check `display.final_response_markdown` instead.

## Verification pattern

After changing to raw mode and restarting, send a short ANSI test with reset codes, e.g. red/green/yellow/blue lines. Ask for a screenshot only if the user is visually verifying a terminal UI; use vision analysis on the screenshot before concluding.

## Pitfalls

- Do not claim colored text rendered correctly without inspecting the actual display when the user provides a screenshot.
- Do not treat `TERM=xterm-256color` or `COLORTERM=truecolor` as sufficient proof; Hermes may still strip/render final responses according to its own display mode.
- Do not store a blanket rule that ANSI is broken. The durable fix is to select the right display mode (`raw`) and restart.

# Example: zl778 Dotfiles Setup

This reference documents the concrete dotfiles repo created in one
session, as a worked example of the `dotfiles-repo-setup` skill.

## Repository

- **Location:** `~/dotfiles/`
- **Remote:** `github.com/zl778/dotfiles`
- **Protocol:** SSH (key registered at GitHub)

## Structure Created

```
~/dotfiles/
├── .gitignore           # Excludes secrets, binary attachments, caches
├── README.md            # Purpose + instructions
├── sync.sh              # cp/rsync from real paths into repo
├── daily-maintenance.sh # hermes update → sync → commit → push
├── home/
│   ├── .zshrc
│   └── .gitconfig
├── bin/                 # ~/.local/bin/ + ~/bin/ mirrored
├── hermes/
│   ├── config.yaml      # API keys replaced with ${VARIABLES}
│   ├── .env.template    # Documented required env vars
│   ├── skills/          # All Hermes skills
│   └── profiles/wukong/ # ChatGPT-OAuth-based coding profile
└── notes/               # Obsidian PARA vault (no attachments)
```

## Secrets Handled

| Original File | In Repo | Reason |
|--------------|---------|--------|
| `~/.hermes/config.yaml` → `api_key: sk-...` | `api_key: ${SILICONFLOW_API_KEY}` | Live key stripped |
| `~/.hermes/.env` | `.gitignore`d | Contains all API keys |
| `~/.hermes/auth.json` | `.gitignore`d | OAuth tokens |

## Daily Cron

- **Schedule:** `0 4 * * *` (every day at 4am)
- **Script:** `~/.hermes/scripts/daily-maintenance.sh`
- **No agent** (pure shell — no LLM cost)
- **Delivers output** to the conversation that created it

## User Profile

- Non-developer (construction/smart-building engineer)
- Uses Obsidian PARA vault via iCloud
- Uses Hermes with multiple providers (DeepSeek + SiliconFlow + Codex OAuth)
- Prefers sync-based approach over symlinks (safety first)

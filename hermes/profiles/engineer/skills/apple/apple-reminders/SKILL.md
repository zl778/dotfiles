---
name: apple-reminders
description: "Apple Reminders via remindctl or osascript: add, list, complete."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Reminders, tasks, todo, macOS, Apple]
prerequisites:
  # remindctl is preferred but optional. When unavailable, use fallback via osascript
  # (references/applescript-native.md) which requires zero dependencies.
  commands: []
---

# Apple Reminders

Use `remindctl` to manage Apple Reminders directly from the terminal. Tasks sync across all Apple devices via iCloud.

## Prerequisites

- **macOS** with Reminders.app
- Install: `brew install steipete/tap/remindctl`
- Grant Reminders permission when prompted
- Check: `remindctl status` / Request: `remindctl authorize`

### Installation Troubleshooting

`remindctl` depends on the system **Command Line Tools (CLT)**. On a fresh or older macOS install, the build chain is sensitive to CLT version. If Homebrew fails with:

```
Error: Your Command Line Tools are too outdated.
Update them from Software Update in System Settings.
```

This is an environment blocker, NOT a skill failure. Do **not** fall back to email for a reminder simply because `remindctl` is unavailable. The correct repair is:

1. Run `xcode-select --install` and complete the system installer, **or**
2. Open **System Settings → General → Software Update** and install the CLT update there, **or**
3. As a last resort, install Xcode from the App Store, then run `sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`

After CLT/Xcode is active, re-run:

```bash
HOMEBREW_NO_AUTO_UPDATE=1 brew install steipete/tap/remindctl
```

If this fails again, run `brew doctor` and inspect its advice before changing strategy.

### Fallback: AppleScript via osascript (no External Dependencies)

When `remindctl` cannot be installed (CLT too old, network issues, tap unavailable), use `osascript` instead — it is built into every macOS system and requires no packages. See [references/applescript-native.md](./references/applescript-native.md) for complete coverage of:

- Creating reminders with due dates and alarms
- Querying reminders by name
- Deleting reminders by name or ID
- Listing all reminder lists

The API surface is slightly different from remindctl (AppleScript blocks vs. CLI flags) but covers all the same operations. Prefer `osascript` when the skill runs in a fresh or unfamiliar macOS environment and `remindctl` fails to install.

## When to Use

- User says **"提醒我" / "remind me"** about a personal task → this is the default handler (see [User Preference](#user-preference-提醒我--apple-reminders-not-agent-cron) below)
- User mentions "reminder" or "Reminders app"
- Creating personal to-dos with due dates that sync to iOS
- Managing Apple Reminders lists
- User wants tasks to appear on their iPhone/iPad

## When NOT to Use

- Calendar events → use Apple Calendar or Google Calendar
- Project task management → use GitHub Issues, Notion, etc.

## User Preference: "提醒我" → Apple Reminders (Not Agent Cron)

Chinese-speaking users on WeChat who say **"提醒我"** (remind me) almost always mean the native Apple Reminders app — notification pops on iPhone/iPad/Mac. **Do not default to Hermes cron.** Only fall back to cron if the user explicitly asks for a WeChat notification or an agent-driven reminder.

Trigger pattern: any "提醒我/提醒我一下/帮我提醒" + time/task content

### View Reminders

```bash
remindctl                    # Today's reminders
remindctl today              # Today
remindctl tomorrow           # Tomorrow
remindctl week               # This week
remindctl overdue            # Past due
remindctl all                # Everything
remindctl 2026-01-04         # Specific date
```

### Manage Lists

```bash
remindctl list               # List all lists
remindctl list Work          # Show specific list
remindctl list Projects --create    # Create list
remindctl list Work --delete        # Delete list
```

### Create Reminders

```bash
remindctl add "Buy milk"
remindctl add --title "Call mom" --list Personal --due tomorrow
remindctl add --title "Meeting prep" --due "2026-02-15 09:00"
```

### Due Time vs Alarm / Early Nudge

`--due` and `--alarm` are different fields:

- `--due` sets the reminder's due date/time.
- `--alarm` sets the EventKit alarm/notification trigger. Timed due reminders may default to an alarm at the due time, but pass `--alarm` explicitly when the user asks for an earlier nudge.

For a reminder due at 2:00 PM with a notification 30 minutes earlier:

```bash
remindctl add --title "Hairdresser" --due "2026-05-15 14:00" --alarm "2026-05-15 13:30"
```

To edit an existing reminder:

```bash
remindctl edit 87354 --due "2026-05-15 14:00" --alarm "2026-05-15 13:30"
```

The Reminders UI may show or group the item by the alarm time because that is when the notification fires. Verify with JSON instead of assuming the due time moved:

```bash
remindctl today --json
```

Expected shape:

- `dueDate`: actual due time
- `alarmDate`: notification / early nudge time

Apple's public `EKReminder` docs list only reminder-specific properties. Alarm support comes from inherited `EKCalendarItem` behavior exposed by remindctl's `--alarm` flag.

### Complete / Delete

```bash
remindctl complete 1 2 3          # Complete by ID
remindctl delete 4A83 --force     # Delete by ID
```

### Output Formats

```bash
remindctl today --json       # JSON for scripting
remindctl today --plain      # TSV format
remindctl today --quiet      # Counts only
```

## Date Formats

Accepted by `--due` and date filters:
- `today`, `tomorrow`, `yesterday`
- `YYYY-MM-DD`
- `YYYY-MM-DD HH:mm`
- ISO 8601 (`2026-01-04T12:34:56Z`)

## User Preference: "提醒我" → Apple Reminders (Not Agent Cron)

Chinese-speaking users on WeChat who say **"提醒我"** almost always mean Apple Reminders — notification pops on iPhone/iPad/Mac via iCloud sync. **Do not default to Hermes cron.**

Trigger pattern: any "提醒我/提醒我一下/帮我提醒" + time/task content → use this skill, not the cronjob tool.

## Rules

1. When user says **"提醒我"** or **"remind me"** in a personal context, default to Apple Reminders (native device push notification via iCloud). See [User Preference](#-user-preference-提醒我--apple-reminders-not-agent-cron) above. Only fall back to Hermes cron if the user explicitly asks for a "微信提醒" or "agent alert".
2. Always confirm reminder content and due date before creating.
3. Use `--json` for programmatic parsing (remindctl) or `log` (osascript).

---
name: macos-app-replacement
description: Safely replace macOS .app bundles using ditto instead of cp -R or rm -rf + cp -R. macOS .app bundles are directories, not files — naive copy approaches leave old files behind.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [macOS, ditto, app-bundle, replacement]
---

# macOS App Bundle Replacement

## The Problem

macOS `.app` bundles are **directories** (packages), not single files. This changes the semantics of common replacement commands:

| Approach | Actual behavior | Result |
|----------|----------------|--------|
| `cp -R new.app /Applications/Old.app` | **Merges** new files INTO the existing Old.app directory | Old files not in new version **survive** → corrupted app |
| `rm -rf /Applications/Old.app && cp -R new.app /Applications/Old.app` | Works but **destructive** — no rollback if something goes wrong | Unwanted risk |
| `ditto new.app /Applications/Old.app` | **Overwrites** the bundle atomically | Clean replacement |

## Safe Method: ditto

```bash
# Replace an existing .app bundle safely
ditto "/path/to/NewVersion.app" "/Applications/Existing.app"

# Replace from a mounted DMG
ditto "/Volumes/AppName/AppName.app" "/Applications/AppName.app"
```

`ditto` is a built-in macOS command (part of BSD subsystem) — no installation needed.

## Verification

```bash
# Compare checksums to confirm replacement
ditto "/Volumes/New.app" "/Applications/Old.app"
md5 -q "/Applications/Old.app"

# Compare against known-good hash from the DMG
md5 -q "/Volumes/New.app/Contents/Info.plist"
# Compare with /Applications/Old.app/Contents/Info.plist
```

## When to Use This Skill

- User updates a macOS app manually (downloading DMG from website)
- Replacing Obsidian, Chrome, or any .app with a new version
- User asks "can I just drag and drop to replace?" — explain why not
- User's .app is broken after a manual "copy over"

## Common Scenarios

### Update Obsidian.app from DMG

```bash
# Mount
hdiutil attach ~/Downloads/Obsidian-1.8.9.dmg

# Replace safely
ditto "/Volumes/Obsidian/Obsidian.app" "/Applications/Obsidian.app"

# Unmount
hdiutil detach "/Volumes/Obsidian"
```

### Update from .zip extraction

```bash
cd ~/Downloads
unzip -q NewApp.zip

# Replace
ditto ./NewApp.app /Applications/ExistingApp.app
```

## Pitfalls

- **`cp -R` onto an existing .app directory merges** — not replaces. This is the most common cause of "app broken after update".
- **`rm -rf /Applications/Some.app` + fresh copy works but has no undo**. If the new version is broken, you've lost the old one. Prefer `ditto`.
- **SIP (System Integrity Protection)** — some system .apps in `/System/Applications/` cannot be replaced at all. Only user-installed apps in `/Applications/` and `~/Applications/` are replaceable.
- **Running apps** — quit the app before replacing (`osascript -e 'quit app "SomeApp"'`). ditto to a running .app may partially succeed but the old in-memory executable keeps running until relaunch.
- **`md5 -q` checks the whole directory tree** — for large .apps this takes a while. Compare individual key files (`Info.plist`, executable binary) for a quicker check.

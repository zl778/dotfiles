# AppleScript 原生操作提醒事项（remindctl 不可用时的 fallback）

当 `remindctl` 因 CLT 版本过旧无法安装时，直接用 `osascript` 操作 Apple Reminders 是最可靠的替代方案。

## 创建提醒

```bash
osascript -e '
tell application "Reminders"
  set newReminder to make new reminder with properties {name:"买菜"}
  set dueDate to (current date)
  set day of dueDate to (day of dueDate) + 1   -- 明天
  set time of dueDate to 9 * hours              -- 09:00
  set due date of newReminder to dueDate
  set remind me date of newReminder to dueDate  -- 到点弹通知
end tell
'
```

### 日期计算说明

- `(current date) + (1 * days)` — 加一天
- `set day of dueDate to (day of dueDate) + 1` — 同效果（加一天）
- `set time of dueDate to 9 * hours` — 设置时间为 09:00
- `set time of dueDate to (9 * hours + 30 * minutes)` — 设置时间为 09:30

### ⚠️ AppleScript 日期陷阱

**不要用** `set due date to (date "09:00" of (due date of r))` — 这会报 `不能将…转换为 specifier 类型` 错误。

正确的做法是先用 `time of dueDate` 或直接赋值 `time of dueDate to 9 * hours`。

## 查询提醒

```bash
osascript -e '
tell application "Reminders"
  set rList to every reminder whose name is "买菜"
  repeat with r in rList
    log "名称: " & name of r
    log "到期: " & (due date of r as text)
    log "提醒闹钟: " & (remind me date of r as text)
  end repeat
end tell
'
```

## 删除提醒（按名称）

```bash
osascript -e '
tell application "Reminders"
  set rList to every reminder whose name is "买菜"
  repeat with r in rList
    delete r
  end repeat
end tell
'
```

## 列出所有列表

```bash
osascript -e '
tell application "Reminders"
  set listNames to name of every list
  repeat with n in listNames
    log "列表: " & n
  end repeat
end tell
'
```

## 性能对比

| 操作 | remindctl | osascript |
|------|-----------|-----------|
| 创建提醒 | ✅ 一行命令 | ✅ 需 AppleScript 块 |
| 查询 | ✅ `--json` 可解析 | ✅ 需手动解析 log |
| 删除 | ✅ `delete <id>` | ✅ 按名称/ID 循环 |
| 安装依赖 | Homebrew + CLT | 无依赖（系统自带） |
| 跨 macOS 版本兼容 | ⚠️ CLT 版本敏感 | ✅ 始终可用 |

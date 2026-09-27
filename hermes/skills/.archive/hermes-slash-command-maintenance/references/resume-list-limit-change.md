# `/resume` 列表上限变更记录

## 适用场景

需要把 Hermes `/resume` 的默认列表从旧数量改为新数量，同时保持 CLI、Gateway 和数字选择一致。

## 本次验证过的实现要点

CLI 侧需要同时检查：

- 空参数 `/resume` 调用显示函数时传入新 `limit`。
- 显示完成后保存到 pending selection 的列表使用同一个 `limit`。
- `/resume N` 重新加载列表时使用同一个 `limit`，否则显示了第 20 条但数字选择仍可能按旧列表判断越界。

Gateway 侧需要同时检查：

- `list_sessions_rich(..., limit=N)` 查询上限。
- 输出前的 `sessions[:N]` 切片。

## 本次环境中的验证路径

Hermes wrapper 使用项目虚拟环境：

```text
/Users/liangzhu/.local/bin/hermes
→ /Users/liangzhu/.hermes/hermes-agent/venv/bin/hermes
```

当系统 `python` 不存在、系统 `python3` 没有 pytest 时，优先尝试：

```bash
./venv/bin/python -m pytest <focused-tests> -q -o addopts=
```

如果虚拟环境也没有 pytest，不要把它描述成代码测试通过；改做：

```bash
./venv/bin/python - <<'PY'
from pathlib import Path
import py_compile

for path in [Path("hermes_cli/cli_commands_mixin.py"),
             Path("gateway/slash_commands.py")]:
    py_compile.compile(str(path), doraise=True)
PY
```

并用源码断言确认查询、渲染切片、pending selection、数字选择均为目标上限。最后用只读命令确认 wrapper 指向的源码可运行：

```bash
./venv/bin/hermes sessions list --limit 20
```

## 生效条件

源码修改后：

- 已运行的 CLI 需要退出并重新启动。
- Gateway 需要 `hermes gateway restart`。

不要直接修改共享 helper 的默认值，除非确实希望 `/history` 等其他命令也改变显示数量；单一命令的需求应在命令调用处传入新上限。

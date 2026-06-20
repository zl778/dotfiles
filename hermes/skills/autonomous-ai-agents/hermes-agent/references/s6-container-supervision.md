# s6-overlay Container Supervision

Architecture reference for the s6-overlay supervision tree inside the Hermes Agent Docker image.

## Architecture

```
/init                                  ← PID 1 (s6-overlay v3.2.3.0)
├── cont-init.d                        ← oneshot setup, runs as root
│   ├── 01-hermes-setup                ← docker/stage2-hook.sh (UID/GID remap, chown, seed, skills sync)
│   └── 02-reconcile-profiles          ← hermes_cli.container_boot (walk profiles → recreate gateway slots)
├── s6-rc.d (static services)
│   ├── main-hermes/run                ← exec sleep infinity (no-op slot)
│   └── dashboard/run                  ← if HERMES_DASHBOARD=1
├── /run/service (s6-svscan watches; tmpfs)
│   └── gateway-<name>/                ← runtime-registered per-profile
└── CMD                                ← /opt/hermes/docker/main-wrapper.sh
```

## Key Files

| Path | Role |
|------|------|
| `Dockerfile` | s6-overlay install + `ENTRYPOINT ["/init", "/opt/hermes/docker/main-wrapper.sh"]` |
| `docker/stage2-hook.sh` | cont-init.d/01 — UID remap, chown, seed, skills sync |
| `docker/cont-init.d/02-reconcile-profiles` | Calls `hermes_cli.container_boot` |
| `docker/main-wrapper.sh` | CMD — routes user args, drops to hermes via s6-setuidgid |
| `hermes_cli/service_manager.py` | `S6ServiceManager` — register/unregister/start/stop |
| `hermes_cli/container_boot.py` | `reconcile_profile_gateways()` |

## Quick Recipes

```sh
# Verify s6 is PID 1
docker exec <c> sh -c 'cat /proc/1/comm; readlink /proc/1/exe'

# Inspect gateway
docker exec <c> /command/s6-svstat /run/service/gateway-<name>

# Manual control
docker exec <c> /command/s6-svc -u /run/service/gateway-<name>   # up
docker exec <c> /command/s6-svc -d /run/service/gateway-<name>   # down

# Watch boot log
docker exec <c> tail -n 50 /opt/data/logs/container-boot.log
```

## Pitfalls

- `/command/` binaries NOT on `docker exec` PATH — always use absolute path
- Profile dirs must be hermes-owned (stage2 chowns every boot)
- Files written by `docker exec` are root-owned — use `--user hermes`
- Reconciler keys on `SOUL.md` presence as "real profile" marker
- Gateway crash loop = unconfigured profile (run `hermes -p <name> setup`)

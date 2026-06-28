# VPS Application Deployment Plan — 10-Service Architecture (2026-06-29)

VPS: `fair-cubes-1` (199.115.228.154, Debian 13, Docker 29.6)
Domain: `61877778.xyz` (Cloudflare DNS)

## Phased deployment order

### Phase 1 — Infrastructure (priority)
| # | Service | Status | URL | Port |
|:-:|:--------|:------:|:----|:---:|
| 1 | **3X-UI** | ✅ Pre-existing | — | — |
| 2 | **Uptime Kuma** | ✅ Done | `uptime.61877778.xyz` | 3001 |
| 3 | **Nginx Proxy Manager** | 🚧 In progress | `199.115.228.154:81` (temp) | 81/8082/4443 |
| 4 | **Vaultwarden** | ✅ Done | `vault.61877778.xyz` | 8080 |

### Phase 2 — Content
| # | Service | Status | URL |
|:-:|:--------|:------:|:----|
| 5 | **Hugo** | ✅ Done | `blog.61877778.xyz` |
| 6 | **FreshRSS** / Miniflux | ❌ Not yet | `rss.61877778.xyz` |

### Phase 3 — Productivity
| # | Service | Status | URL |
|:-:|:--------|:------:|:----|
| 7 | **n8n** | ❌ Not yet | `flow.61877778.xyz` |
| 8 | **Memos** | ❌ Not yet | `memo.61877778.xyz` |

### Phase 4 — Ops
| # | Service | Status | URL |
|:-:|:--------|:------:|:----|
| 9 | **File Browser** | ❌ Not yet | `files.61877778.xyz` |
| 10 | **Beszel** | ❌ Not yet | `monitor.61877778.xyz` |

## Current Nginx configuration

All proxies run through **system Nginx** (not NPM yet):

| Subdomain | Upstream | SSL |
|:----------|:---------|:---:|
| `vault.61877778.xyz` | `127.0.0.1:8080` | acme.sh ECDSA |
| `uptime.61877778.xyz` | `127.0.0.1:3001` | acme.sh ECDSA |
| `blog.61877778.xyz` | Cloudflare Pages (external) | CF managed |

## Port allocation

| Port | Used by |
|:----:|:--------|
| 22 | SSH |
| 80 | System Nginx (HTTP → 301) |
| 443 | System Nginx (HTTPS) |
| 81 | NPM admin UI (coexistence) |
| 2053 | 3X-UI |
| 3001 | Uptime Kuma |
| 8080 | Vaultwarden |
| 8082 | NPM HTTP (coexistence) |
| 4443 | NPM HTTPS (coexistence) |

## Migration plan (system Nginx → NPM)

1. Deploy NPM on alt ports (81, 8082, 4443) — done
2. Add proxy hosts in NPM UI for all existing services
3. Get SSL certs through NPM's built-in ACME
4. Stop system Nginx: `systemctl stop nginx`
5. Reconfigure NPM: change ports from 8082→80, 4443→443
6. Update UFW if needed
7. Remove old system Nginx site configs

## Notes

- `:latest` Docker tag often lags behind GitHub releases — always check Docker Hub tags
- acme.sh auto-renewal is registered via `--install-cert --reloadcmd`
- Named Docker volumes persist across container re-creation
# VPS Application Deployment Plan — 10-Service Architecture (2026-06-29)

VPS: `fair-cubes-1` (199.115.228.154, Debian 13, Docker 29.6)
Domain: `61877778.xyz` (Cloudflare DNS, all services gray cloud)
Reverse proxy: **Nginx Proxy Manager** (system Nginx retired)

## Phased deployment order

### Phase 1 — Infrastructure (priority)
| # | Service | Status | URL | Port |
|:-:|:--------|:------:|:----|:----:|
| 1 | **3X-UI** | ✅ Pre-existing | — | — |
| 2 | **Uptime Kuma** | ✅ Done | `uptime.61877778.xyz` | 3001 |
| 3 | **Nginx Proxy Manager** | ✅ Done, system Nginx retired | `npm.61877778.xyz` | 81 (admin) / 80/443 (proxy) |
| 4 | **Vaultwarden** | ✅ Done | `vault.61877778.xyz` | 8080 |

### Phase 2 — Content
| # | Service | Status | URL |
|:-:|:--------|:------:|:----|
| 5 | **Hugo** | ✅ Done | `blog.61877778.xyz` (Cloudflare Pages) |
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
| 10 | **Beszel** | ✅ Done | `beszel.61877778.xyz` |

## Current Nginx configuration

All proxy through **Nginx Proxy Manager** (system Nginx fully retired):

| Subdomain | Docker container | Container IP | Internal port |
|:----------|:-----------------|:-------------|:-------------:|
| `vault.61877778.xyz` | vaultwarden | `172.17.0.2` | 80 |
| `uptime.61877778.xyz` | uptime-kuma | `172.17.0.3` | 3001 |
| `npm.61877778.xyz` | nginx-proxy-manager | `172.17.0.4` | 81 |
| `beszel.61877778.xyz` | beszel | `172.17.0.5` | 8090 |
| `blog.61877778.xyz` | — (Cloudflare Pages) | external | — |

**Important: NPM uses container Docker bridge IPs (not 127.0.0.1) for forwarding.**
Get container IP: `docker inspect <name> --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'`

## Port allocation

| Port | Used by | Note |
|:----:|:--------|:-----|
| 22 | SSH | — |
| 80 | NPM (HTTP redirect → HTTPS) | NPM managed |
| 81 | NPM admin UI | NPM managed |
| 443 | NPM (HTTPS) | NPM auto SSL |
| 2053 | 3X-UI | — |
| 3001 | Uptime Kuma | — |
| 45876 | Beszel Agent | host network, no port mapping |
| 8080 | Vaultwarden | — |
| 8090 | Beszel Hub | — |

## Migration history

System Nginx was retired on 2026-06-29. All proxy rules moved to NPM.
- Old system Nginx site configs: `/etc/nginx/sites-enabled/vaultwarden`, `uptime`, `npm` (removed)
- Old SSL certs via acme.sh: vault.61877778.xyz, uptime.61877778.xyz, npm.61877778.xyz
- New SSL certs: NPM auto-managed Let's Encrypt (grey cloud DNS required)

## Notes

- `:latest` Docker tag often lags behind GitHub releases — check Docker Hub tags and pin when upgrading
- Named Docker volumes persist across container re-creation
- All NPM-managed domains use **grey cloud** (DNS only) in Cloudflare — orange cloud breaks Let's Encrypt ACME challenges
- Block Common Exploits should be enabled for every proxy host
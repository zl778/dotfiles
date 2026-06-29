---
name: vps-docker-deployment
description: Deploy Docker-based self-hosted services on a VPS with Nginx Proxy Manager, SSL, and monitoring
---

# VPS Docker Service Deployment

Deploy Docker-based self-hosted services on a Linux VPS (Debian/Ubuntu), route them through Nginx Proxy Manager (NPM) for unified SSL management, and wire up monitoring.

## Prerequisites

- SSH root access to VPS
- Docker Engine installed
- Domain managed via Cloudflare (**grey cloud** / DNS-only — NPM handles SSL)
- Nginx Proxy Manager already deployed on ports 80:80, 443:443, 81:81
- Custom Docker network for inter-container communication (e.g. `beszel-net`, `npm-net`)

## Standard Workflow

### 1. Cloudflare DNS

| Type | Name | Target |
|:---:|:----|:------|
| A | `subdomain` | `VPS_IP` |

Cloud = **grey** (DNS only). Orange cloud (proxied) breaks Let's Encrypt ACME challenges because NPM sees Cloudflare's IP, not the VPS.

### 2. Docker Container

```bash
# Pull image
docker pull image:tag

# Run with port mapping + volume
docker run -d --restart unless-stopped \
  --name service-name \
  --network beszel-net \
  -p HOST_PORT:CONTAINER_PORT \
  -v volume-name:/data \
  IMAGE
```

**CRITICAL:** Do NOT use `127.0.0.1` as the forward target in NPM. Inside a Docker container, `127.0.0.1` refers to the container itself, not the host. Use the container's actual IP on the Docker network (check via `docker inspect`).

### 3. NPM Reverse Proxy

In NPM web UI (https://npm.yourdomain.com):

**Details tab:**
- Domain Names: `subdomain.yourdomain.com`
- Scheme: `http` (internal, even for HTTPS sites — NPM terminates SSL)
- Forward IP: Container IP (e.g. `172.20.0.3`)
- Forward Port: Container's internal port
- Block Common Exploits: ✅

**SSL tab:**
- Select **Request a new Certificate**
- NPM auto-renews via Let's Encrypt

### 4. Verify

```bash
curl -s -o /dev/null -w "HTTP %{http_code}" https://subdomain.yourdomain.com
```

## Migration from System Nginx to NPM

```bash
# 1. Stop system Nginx
systemctl stop nginx
killall nginx

# 2. Recreate NPM on 80/443 (was on alt ports)
docker rm -f nginx-proxy-manager
docker run -d --restart always --name nginx-proxy-manager \
  -p 80:80 -p 443:443 -p 81:81 \
  -v npm-data:/data -v npm-letsencrypt:/etc/letsencrypt \
  jc21/nginx-proxy-manager:latest

# 3. In NPM UI, add all proxy hosts (old + new)
# 4. Update Cloudflare DNS to grey cloud for all domains
```

## Service-Specific References

See `references/` files for per-service deployment details:

- `references/uptime-kuma.md`
- `references/vaultwarden.md`
- `references/beszel.md`
- `references/npm.md`

## Common Pitfalls

### 502 Bad Gateway
- **Cause:** Incorrect forward IP in NPM — `127.0.0.1` inside container != host
- **Fix:** Use the container's Docker network IP (`docker inspect <name> | grep IPAddress`)

### SSL Cert Failure (500 Internal Error)
- **Cause:** NPM can't bind port 80 for ACME challenge if another service occupies it
- **Fix:** Ensure NPM owns ports 80/443 and no system Nginx or other process is on them

### Beszel Agent Offline
- **Cause:** Hub and Agent on different Docker networks, or wrong host/IP in Hub
- **Fix:** Put both on same custom network; use Agent's container IP in Hub config

### Uptime Kuma — No "SSL Certificate" Monitor Type
- In v2.x, SSL cert monitoring is a checkbox under HTTP(s) monitor's **Advanced** settings, not a standalone type

## Architecture

```
Cloudflare (grey DNS only)
  │
NPM (80/443) ── unified SSL + reverse proxy
  ├── vault.yourdomain.com  →  Vaultwarden
  ├── uptime.yourdomain.com →  Uptime Kuma
  ├── npm.yourdomain.com    →  NPM admin UI
  └── beszel.yourdomain.com →  Beszel Hub

Beszel Hub
  └── fair-cubes-1 (Agent)  →  CPU / RAM / Disk / Docker
```

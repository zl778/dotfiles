# Nginx Proxy Manager Deployment (2026-06-29)

Deployment of Nginx Proxy Manager on fair-cubes-1 VPS, replacing system Nginx.

## Service details

| Item | Value |
|:----|:------|
| Admin URL | `https://npm.61877778.xyz` |
| Subdomain | `npm` (Cloudflare gray DNS) |
| Docker image | `jc21/nginx-proxy-manager:latest` |
| Admin port | 81 |
| Proxy ports | 80 (HTTP), 443 (HTTPS) — after migration |
| Volumes | `npm-data:/data`, `npm-letsencrypt:/etc/letsencrypt` |
| Default login | admin@example.com / changeme |
| SSL (initial) | acme.sh via system Nginx |
| SSL (after migration) | NPM auto-managed Let's Encrypt |

## Deployment strategy: migrate from system Nginx

System Nginx was already running on 80/443 serving Vaultwarden and Uptime Kuma. Two-step migration:

### Phase 1 — Coexistence (NPM on alt ports)

```bash
# Run NPM on alternative ports to avoid conflict with system Nginx
docker run -d --restart always --name nginx-proxy-manager \\
  -p 81:81 -p 8082:80 -p 4443:443 \\
  -v npm-data:/data \\
  -v npm-letsencrypt:/etc/letsencrypt \\
  jc21/nginx-proxy-manager:latest
```

- Admin UI accessed at `http://<VPS-IP>:81` (no SSL yet)
- Set up a temporary Nginx reverse proxy for `npm.61877778.xyz` → `127.0.0.1:81` with SSL to provide HTTPS access during setup

### Phase 2 — Switch (NPM takes 80/443)

```bash
# 1. Stop system Nginx
systemctl stop nginx 2>/dev/null; killall nginx 2>/dev/null
sleep 1

# 2. Remove old NPM container, recreate with 80/443
docker stop nginx-proxy-manager
docker rm nginx-proxy-manager
docker run -d --restart always --name nginx-proxy-manager \\
  -p 80:80 -p 443:443 -p 81:81 \\
  -v npm-data:/data \\
  -v npm-letsencrypt:/etc/letsencrypt \\
  jc21/nginx-proxy-manager:latest
```

### Phase 3 — Add proxy hosts in NPM

After switching, all old services go down until proxy hosts are added in NPM:

| Domain | Forward to | Service |
|:-------|:-----------|:--------|
| `vault.61877778.xyz` | `127.0.0.1:8080` | Vaultwarden |
| `uptime.61877778.xyz` | `127.0.0.1:3001` | Uptime Kuma |
| `npm.61877778.xyz` | `127.0.0.1:81` | NPM itself |

For each proxy host:
1. **Details tab**: Domain, scheme `http`, forward IP `127.0.0.1`, forward port, enable **Block Common Exploits**
2. **SSL tab**: Select **Request a new Certificate** (NPM auto-manages Let's Encrypt — no acme.sh needed)
   - No email field on this page — set **Default Let's Encrypt Email** in **Settings** (gear icon) first
   - NPM has direct access to port 80, so ACME challenge succeeds immediately
3. Click **Save** — SSL cert is issued and installed automatically

## Pitfalls

1. **Let's Encrypt email missing** — The email field is not on the SSL tab. Set it globally under **Settings → Default Let's Encrypt Email** before requesting certs.

2. **Downtime during switch** — Between stopping system Nginx and adding proxy hosts in NPM, all services are down. Add proxy hosts promptly.

3. **Docker volume persistence** — Named volumes (`npm-data`, `npm-letsencrypt`) survive container recreation. Proxy host configs and certs are preserved across upgrades.

4. **Nginx orphaned PIDs** — After stopping system Nginx, `systemctl stop nginx` may leave zombie PIDs. Run `killall nginx 2>/dev/null` for cleanup before starting NPM on 80/443.

## Comparison: system Nginx vs NPM

| Aspect | System Nginx | NPM |
|:-------|:------------|:----|
| Config management | Manual file editing via SSH | Web UI |
| SSL certs | acme.sh CLI | Auto via Let's Encrypt |
| Add new domain | Write Nginx config + get cert | Click 3 fields + Save |
| Resource usage | Very low (~20MB) | ~150MB (Node.js-based) |
| Migration | — | Migrate all existing domains or keep hybrid |

## Related

- `references/uptime-kuma-deployment.md` — Uptime Kuma setup on same VPS
- `references/vps-application-plan.md` — Full deployment roadmap
- `vps-server-backup` skill — VPS backup configuration
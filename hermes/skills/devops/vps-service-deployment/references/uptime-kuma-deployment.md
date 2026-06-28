# Uptime Kuma Deployment (2026-06-29)

Deployment of Uptime Kuma on fair-cubes-1 VPS (199.115.228.154, Debian 13).

## Service details

| Item | Value |
|:----|:------|
| URL | `https://uptime.61877778.xyz` |
| Subdomain | `uptime` (Cloudflare gray DNS) |
| Docker image | `louislam/uptime-kuma:2.4.0` (pinned, not :latest) |
| Internal port | 3001 |
| Volume | `uptime-kuma` named volume (`/app/data`) |
| SSL | Let's Encrypt ECDSA via acme.sh |
| SSL cert path | `/etc/ssl/certs/uptime.fullchain.pem` |
| SSL key path | `/etc/ssl/private/uptime.key` |
| Nginx config | `/etc/nginx/sites-enabled/uptime.conf` |

## Commands used

### Docker run

```bash
docker run -d --restart always \\
  -p 3001:3001 \\
  -v uptime-kuma:/app/data \\
  --name uptime-kuma \\
  louislam/uptime-kuma:latest
```

### Nginx config (initial HTTP)

Wrote to `/etc/nginx/sites-enabled/uptime.conf` with:
- proxy_pass to 127.0.0.1:3001
- WebSocket headers included
- server_name `uptime.61877778.xyz`

### SSL cert (standalone, stopped Nginx)

```bash
systemctl stop nginx
nginx -s stop
~/.acme.sh/acme.sh --issue -d uptime.61877778.xyz --standalone --keylength ec-256
```

### Install cert + auto-renewal

```bash
~/.acme.sh/acme.sh --install-cert -d uptime.61877778.xyz --ecc \\
  --fullchain-file /etc/ssl/certs/uptime.fullchain.pem \\
  --key-file /etc/ssl/private/uptime.key \\
  --reloadcmd "nginx -s reload"
```

### Nginx config (final with HTTPS + HTTP redirect)

Updated to:
- HTTPS on 443 with http2
- HTTP on 80 redirecting to HTTPS (301)

**Pitfall encountered:** `listen 443 ssl http2;` triggered a deprecation warning. Fixed with `listen 443 ssl; http2 on;`.

### DNS

Cloudflare A record: `uptime` -> `199.115.228.154` (gray cloud)

### First access

Browser returned 302 (redirect to /dashboard), showing Uptime Kuma setup page.

## Version upgrade

Initial deployment used `:latest` (1.23.17). GitHub release showed 2.4.0 available.

**Docker Hub tag discovery:**

```bash
curl -s "https://hub.docker.com/v2/repositories/louislam/uptime-kuma/tags?page_size=10" \\
  | python3 -c "import sys,json; data=json.load(sys.stdin); [print(t['name']) for t in data.get('results',[])]"
```

Found `2.4.0` tag available. The `:latest` tag was still pointing at 1.23.17.

**Upgrade:**
```bash
docker pull louislam/uptime-kuma:2.4.0
docker stop uptime-kuma
docker rm uptime-kuma
docker run -d --restart always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:2.4.0
```

Volume persisted across container recreation - no data loss.

## Current state

- Version 2.4.0 verified (from `/app/package.json`)
- Container healthy
- HTTPS accessible (login page shown, user created admin account)

The user was shown the dashboard and will add monitors (uptime.61877778.xyz, vault.61877778.xyz, blog.61877778.xyz, VPS ping, SSL expiry checks) and configure Telegram notifications.

## Notes

- Backing up the container data: `docker run --rm -v uptime-kuma:/data -v /backups:/backup alpine tar czf /backup/uptime-kuma-$(date +%Y%m%d).tar.gz -C /data .`
- This service is independent from Vaultwarden - no shared data dependencies.
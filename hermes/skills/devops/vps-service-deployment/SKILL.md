---
name: vps-service-deployment
description: Deploy a Docker-based web service on a VPS with Nginx reverse proxy, acme.sh SSL, and Cloudflare DNS. Covers the full lifecycle from container setup to HTTPS verification.
tags:
  - devops
  - vps
  - docker
  - nginx
  - ssl
  - vps-server-mgmt
---

# VPS Service Deployment

Deploy a Docker-based web service on a remote Linux VPS with Nginx reverse proxy, Let's Encrypt SSL via acme.sh, and Cloudflare DNS. This skill captures the repeatable pattern used across multiple services (Vaultwarden, Uptime Kuma, etc.).

## When to use

User wants to add a new self-hosted service to their VPS. The service runs in a Docker container and needs a public HTTPS URL.

## Standard deployment workflow

### Step 1 - Start the Docker container

```bash
ssh root@<VPS-IP> '
  docker run -d \\
    --restart always \\
    -p <PORT>:<CONTAINER_PORT> \\
    -v <VOLUME_NAME>:/app/data \\
    --name <SERVICE-NAME> \\
    <IMAGE>:<TAG>
'
```

Verify:
```bash
ssh root@<VPS-IP> 'docker ps --format "table {{.Names}}\t{{.Status}}"'
```

### Step 2 - Create Nginx reverse proxy (HTTP, for SSL issuance)

```bash
ssh root@<VPS-IP> 'cat > /etc/nginx/sites-enabled/<SERVICE>.conf << "NGINXEOF"
server {
    listen 80;
    server_name <SUBDOMAIN>.<DOMAIN>;
    location / {
        proxy_pass http://127.0.0.1:<PORT>;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # WebSocket support (needed for some services)
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
NGINXEOF
nginx -t && nginx -s reload'
```

### Step 3 - Get SSL cert (acme.sh standalone)

acme.sh standalone needs port 80 free, so stop Nginx first:

```bash
ssh root@<VPS-IP> '
  systemctl stop nginx 2>/dev/null; nginx -s stop 2>/dev/null
  sleep 1
  ~/.acme.sh/acme.sh --issue -d <SUBDOMAIN>.<DOMAIN> --standalone --keylength ec-256
'
```

### Step 4 - Install cert + auto-renewal

```bash
ssh root@<VPS-IP> '
  mkdir -p /etc/ssl/certs /etc/ssl/private
  ~/.acme.sh/acme.sh --install-cert -d <SUBDOMAIN>.<DOMAIN> --ecc \\
    --fullchain-file /etc/ssl/certs/<SERVICE>.fullchain.pem \\
    --key-file /etc/ssl/private/<SERVICE>.key \\
    --reloadcmd "nginx -s reload"
'
```

### Step 5 - Update Nginx with HTTPS

**Nginx 1.25+ deprecated `listen ... http2`** - use `listen 443 ssl; http2 on;` instead.

```bash
ssh root@<VPS-IP> 'cat > /etc/nginx/sites-enabled/<SERVICE>.conf << "NGINXEOF"
server {
    listen 443 ssl;
    http2 on;
    server_name <SUBDOMAIN>.<DOMAIN>;

    ssl_certificate /etc/ssl/certs/<SERVICE>.fullchain.pem;
    ssl_certificate_key /etc/ssl/private/<SERVICE>.key;

    location / {
        proxy_pass http://127.0.0.1:<PORT>;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

server {
    listen 80;
    server_name <SUBDOMAIN>.<DOMAIN>;
    return 301 https://\$host\$request_uri;
}
NGINXEOF
nginx -t && nginx -s reload'
```

### Step 6 - Add Cloudflare DNS record

User adds an A record in Cloudflare dashboard:

| Type | Name | Target |
|:---:|:----|:------|
| A | `<SUBDOMAIN>` | `<VPS-IP>` |

Set to gray cloud (DNS only) - not orange (proxied).

### Step 7 - Verify HTTPS

```bash
curl -sI --connect-timeout 5 https://<SUBDOMAIN>.<DOMAIN>/ 2>&1 | head -5
```

Should return HTTP/2 200 (or 302 for first-time setup pages).

## Pitfalls

1. **Nginx http2 syntax** - Nginx 1.25+ no longer allows `listen 443 ssl http2;`. Use `listen 443 ssl;` + `http2 on;`.

2. **acme.sh standalone needs port 80** — Must stop Nginx before issuing (`systemctl stop nginx 2>/dev/null; nginx -s stop 2>/dev/null`). After cert is issued, start fresh with `nginx` (not `nginx -s reload`, because pid file was deleted on full stop). Restart immediately after.

3. **WebSocket headers** - Always include `Upgrade` and `Connection` proxy headers even for non-WebSocket services; avoids later reconfiguration.

4. **Cloudflare orange cloud** - For self-hosted services, use gray (DNS only). Orange (proxied) breaks WebSocket, real IP, and cert challenges.

5. **Docker :latest lag** - The `latest` tag often lags behind GitHub releases. Check Docker Hub tags and pin to explicit version when upgrading.

6. **UFW port 443** - Must be open. Check with `ufw status | grep 443`. If missing: `ufw allow 443/tcp`.

7. **acme.sh auto-renewal** - `--install-cert` with `--reloadcmd` registers the renewal cron automatically. Verify: `crontab -l | grep acme`.

8. **Named Docker volumes persist** - When recreating containers, named volumes (`-v <NAME>:/data`) survive `docker rm`. Data is safe.

9. **Port conflict with existing Nginx** - When deploying tools that want ports 80/443 (e.g., Nginx Proxy Manager, Caddy) on a VPS already running system Nginx:
   - **Coexistence strategy**: Run the new tool on **alternative ports** (e.g., web UI on 81, HTTP on 8082, HTTPS on 4443). Keep system Nginx on 80/443.
   - **Migration strategy**: Configure all proxy rules in the new tool first (using the alternative ports), then switch — stop system Nginx, reconfigure the new tool to use 80/443 directly.
   - **Check ports in use before deploying**: `ssh root@<VPS-IP> 'ss -tlnp | grep -E \" (80|443)\"'` to see if ports are occupied before choosing a strategy.
   - **After switching 80/443, old proxy hosts are down until reconfigured** — The new tool (NPM, Caddy, etc.) starts blank. Add proxy hosts for all existing services before or immediately after switching to minimize downtime.

10. **Nginx orphaned PIDs after stop** — `nginx -s stop` can leave zombie processes that still hold ports. If restarting Nginx fails with "Address already in use", check with `ss -tlnp | grep nginx` and kill leftover PIDs with `kill -9 <PID>`. Then start fresh with `nginx` (not `nginx -s reload`).

11. **acme.sh reloadcmd fails after full stop** — `--reloadcmd "nginx -s reload"` fails with `open() "/run/nginx.pid" failed` when Nginx was fully stopped (pid file deleted). Restart Nginx with `nginx` or `systemctl start nginx` first, then the reloadcmd works on subsequent renewals.

12. **Docker :latest tag vs GitHub releases** — The Docker Hub `:latest` tag often lags behind GitHub releases by several versions. Check available tags via Docker Hub API (`curl -s "https://hub.docker.com/v2/repositories/<ORG>/<IMAGE>/tags?page_size=10" | python3 -c "import sys,json; data=json.load(sys.stdin); [print(t['name']) for t in data.get('results',[])]"`) and pin to the latest semantic version tag instead of `:latest`.

13. **Uptime Kuma 2.4.0 — SSL cert monitoring moved** — In version 2.4.0, SSL certificate monitoring is no longer a separate monitor type. It's now integrated into **HTTP(s)** monitors as an advanced option: add an HTTP(s) monitor, scroll to **高级 (Advanced)** section, check **「证书到期时通知」** (Notify on certificate expiration). Same monitor tracks both uptime AND certificate expiry.

14. **NPM Docker networking — `127.0.0.1` is container-local** — Inside the NPM container, `127.0.0.1` refers to the NPM container itself, not the host machine. Using it as the forward IP causes **502 Bad Gateway**. Use the backend container's actual Docker bridge IP instead:
    ```bash
    docker inspect <container-name> --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
    ```
    In NPM Proxy Hosts → Forward Hostname/IP: use that IP (e.g. `172.17.0.2`)
    Forward Port: use the **container's internal port** (e.g. `80` for Vaultwarden, not the host-mapped `8080`)

15. **Beszel — Hub first, then Agent** — Beszel has two components:
    - **Hub** (management UI): Docker container on port 8090
    - **Agent** (data collector): Needs an **authentication key generated by the Hub** — cannot run standalone.
    Workflow: deploy Hub → open web UI → create admin account → add a system (Hub generates a key command) → copy and run the agent command with the key.

16. **Uptime Kuma vs Beszel — not redundant** — They serve complementary roles:
    - **Uptime Kuma**: external monitoring ("Can users access the service from outside?") — HTTP status, Ping, SSL expiry
    - **Beszel**: internal monitoring ("How is the VPS itself doing?") — CPU, memory, disk, Docker containers
    Analogy: Uptime Kuma = 门口保安 (checks external access), Beszel = 水电表 (checks internal resources).

## Verification checklist

```bash
# 1. Container running
docker ps | grep <SERVICE>

# 2. Local port accessible
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:<PORT>

# 3. HTTPS publicly accessible
curl -sI https://<SUBDOMAIN>.<DOMAIN>/

# 4. SSL cert valid 80+ days
ssh root@<VPS-IP> 'openssl x509 -enddate -noout -in /etc/ssl/certs/<SERVICE>.fullchain.pem'

# 5. Nginx config valid
ssh root@<VPS-IP> 'nginx -t'

# 6. Auto-renewal registered
ssh root@<VPS-IP> 'crontab -l | grep acme'
```

## Reference

- `references/npm-deployment.md` — Nginx Proxy Manager deployment with system Nginx migration
- `references/uptime-kuma-deployment.md` — Complete Uptime Kuma session transcript
- `references/beszel-deployment.md` — Beszel Hub + Agent deployment

## Related skills

- `vps-server-backup` - Automated backup scripts on the same VPS
- `vps-server-backup/references/security-contingency-plan.md` - Security contingency plan template for any service
- `references/vps-application-plan.md` - Full 10-service deployment roadmap for this VPS
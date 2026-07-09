# NPM — Nginx Proxy Manager

Reverse proxy + SSL management web UI.

## Fresh Install
```bash
docker run -d --restart always \
  --name nginx-proxy-manager \
  -p 80:80 -p 443:443 -p 81:81 \
  -v npm-data:/data \
  -v npm-letsencrypt:/etc/letsencrypt \
  jc21/nginx-proxy-manager:latest
```

- Admin UI: http://VPS_IP:81
- Default login: `admin@example.com` / `changeme`

## Migration from System Nginx

When moving from manually-configured system Nginx to NPM:

```bash
# 1. Stop system Nginx
systemctl stop nginx
killall nginx

# 2. Recreate NPM on 80/443 (if previously on alt ports)
docker rm -f nginx-proxy-manager
docker run -d --restart always --name nginx-proxy-manager \
  -p 80:80 -p 443:443 -p 81:81 \
  -v npm-data:/data -v npm-letsencrypt:/etc/letsencrypt \
  jc21/nginx-proxy-manager:latest

# 3. In NPM UI, add each service as a Proxy Host
# 4. Update all Cloudflare DNS to grey cloud
```

## Adding a Proxy Host

**Details:**
- Domain Names: `sub.yourdomain.com`
- Scheme: `http` (NPM terminates SSL)
- Forward IP: **Container IP** (NOT 127.0.0.1 — see pitfall below)
- Forward Port: Container's internal port
- Block Common Exploits: ✅

**SSL:**
- Request a new Certificate

## ⚠️ CRITICAL: The 127.0.0.1 Pitfall

Inside a Docker container, `127.0.0.1` refers to the **container itself**, not the host machine.

✅ **Correct:** use the target container's Docker network IP
```bash
docker inspect <service-name> | grep IPAddress
# → 172.17.0.2, 172.20.0.3, etc.
```
❌ **Wrong:** `127.0.0.1` or `172.17.0.1` (Docker gateway)

Symptom: 502 Bad Gateway from NPM.

## Default Login
- Email: `admin@example.com`
- Password: `changeme`
- (Changes on first login)
# Uptime Kuma Deployment

**Uptime Kuma** = external uptime monitoring with Telegram alerts

## Docker
```bash
docker run -d --restart always \
  -p 3001:3001 \
  -v uptime-kuma:/app/data \
  --name uptime-kuma \
  louislam/uptime-kuma:2.4.0
```

Note: Use tag `2.4.0` explicitly (`:latest` was still 1.23.17 as of June 2026)

## NPM Proxy
- Domain: `uptime.yourdomain.com`
- Forward: `CONTAINER_IP:3001`
- SSL: Request new certificate

## First Setup
1. Open https://uptime.yourdomain.com
2. Create admin account
3. Add monitors:
   - HTTP(s) → `https://uptime.yourdomain.com` (self-monitor)
   - HTTP(s) → `https://vault.yourdomain.com` + Advanced: check "证书到期时通知"
   - Ping → `VPS_IP`

## Telegram Notification
Settings → Notifications → Add Telegram:
- Bot Token: from @BotFather
- Chat ID: your group/user ID
- Test → Save

## SSL Certificate Monitoring
In v2.x, SSL cert monitoring is NOT a separate monitor type.
Check **"证书到期时通知"** under Advanced settings of an HTTP(s) monitor.
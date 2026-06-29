# Vaultwarden Deployment

**Vaultwarden** = self-hosted Bitwarden-compatible password manager

## Docker

```bash
docker run -d --restart unless-stopped \
  --name vaultwarden \
  -v /vw-data/:/data/ \
  -p 8080:80 \
  vaultwarden/server:latest
```

## NPM Proxy

- Domain: `vault.yourdomain.com`
- Forward: `CONTAINER_IP:80` (internal port, not host port 8080)
- SSL: Request new certificate

## Backup

```bash
# VPS backup script
cat > /usr/local/bin/vaultwarden-backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups"
mkdir -p $BACKUP_DIR
FILENAME="vw-$(date +%Y%m%d).tar.gz"
tar czf "$BACKUP_DIR/$FILENAME" -C / vw-data/
find $BACKUP_DIR -name "vw-*.tar.gz" -mtime +7 -delete
echo "[$(date "+%Y-%m-%d %H:%M:%S")] 备份完成: $FILENAME ($(du -h "$BACKUP_DIR/$FILENAME" | cut -f1))" >> /var/log/vaultwarden-backup.log
EOF
chmod +x /usr/local/bin/vaultwarden-backup.sh

# Cron: daily 3:00 AM
(crontab -l 2>/dev/null; echo "0 3 * * * /usr/local/bin/vaultwarden-backup.sh") | crontab -
```

## Security

- **Master password is unrecoverable** — zero-knowledge architecture
- Store master password physically AND in another password manager (e.g. Apple Keychain)
- Enable 2FA and save recovery codes

See `Vaultwarden安全预案.md` in dotfiles for full contingency plan.
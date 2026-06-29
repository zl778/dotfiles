# Beszel Deployment

**Beszel** = lightweight system resource monitoring (CPU, RAM, Disk, Bandwidth, Docker containers)

## Architecture

- **Hub** (Web UI): `henrygd/beszel`, port 8090
- **Agent** (data collector): `henrygd/beszel-agent`, port 45876
- Hub connects **to** Agent via SSH (agent is SSH server, hub is client)

## Deployment

### 1. Create shared network
```bash
docker network create beszel-net
```

### 2. Hub
```bash
docker run -d --restart always \\\n  --name beszel \\\n  --network beszel-net \\\n  -p 8090:8090 \\\n  -v beszel-data:/beszel/data \\\n  henrygd/beszel:latest
```

Add to NPM: `beszel.yourdomain.com` → CONTAINER_IP:8090 (http) + SSL

### 3. In Hub UI
1. Create admin account
2. Click **+ 添加系统** → fill:
   - Name: `fair-cubes-1`
   - Host/IP: Agent's container IP (check after step 4)
   - Port: `45876`
3. Copy the generated `docker run` command

### 4. Agent
Run the command from Hub, but ensure `--network beszel-net` is included

### 5. Update Hub config
After agent is running, note its IP and update Host/IP in Hub.

## Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| "no key provided" | Missing `KEY` env var | Add from Hub |
| "must set TOKEN" | Missing `TOKEN` env var | Add from Hub |
| WebSocket 401/400 | Wrong token or IP mismatch | Re-add system; check IP |
| Hub shows Offline | Different networks | Same custom network; use container IP |
| "Collecting data..." forever | Just started | Wait 1-2 min |

## Resource Usage
- Hub: ~13 MB RAM
- Agent: ~7 MB RAM

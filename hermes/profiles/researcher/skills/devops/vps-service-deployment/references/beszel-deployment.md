# Beszel — 轻量服务器监控

## 架构

- **Beszel Hub** — Web 管理界面，收集并展示监控数据（端口 8090）
- **Beszel Agent** — 每台被监控机器上安装一个，采集 CPU/内存/磁盘/Docker 数据

## 部署步骤

### 1. 启动 Hub
```bash
docker run -d --restart always -p 8090:8090 --name beszel henrygd/beszel:latest
```

### 2. 打开 Web UI 创建管理员账号
浏览器访问 `http://<VPS-IP>:8090`（或通过 NPM 配好域名后走 HTTPS）

### 3. 添加系统获取密钥
在 Hub UI → Add System → 填写名称/IP/端口 → Hub 生成 docker-compose（含 KEY + TOKEN + HUB_URL）

**两种启动 Agent 的方式：**

**方式 A：docker run（通过环境变量）**
```bash
docker run -d --restart unless-stopped --name beszel-agent --network host \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /opt/beszel-agent/data:/var/lib/beszel-agent \
  -e LISTEN=45876 \
  -e KEY="<公钥>" \
  -e TOKEN="<令牌>" \
  -e HUB_URL="https://beszel.<域名>" \
  henrygd/beszel-agent:latest
```

**方式 B：docker-compose（从 Hub 复制）**
```yaml
services:
  beszel-agent:
    image: henrygd/beszel-agent
    container_name: beszel-agent
    restart: unless-stopped
    network_mode: host
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./beszel_agent_data:/var/lib/beszel-agent
    environment:
      LISTEN: 45876
      KEY: '<公钥>'
      TOKEN: '<令牌>'
      HUB_URL: 'https://beszel.<域名>'
```

**重要：`network_mode: host` 意味着不要用 `-p` 映射端口，Agent 直接监听宿主机的 45876 端口。**

## NPM 代理配置
- 域名：`beszel.61877778.xyz`
- Forward IP：`172.17.0.x`（docker inspect beszel）
- Forward Port：`8090`
- SSL：Let's Encrypt（通过 NPM 自动申请）

## 注意事项
- **Agent 不能先启动** — 必须先通过 Hub 生成密钥，带密钥启动
- **Agent 需要访问 Docker socket** 才能监控容器状态
- **Token 必须与 Hub 生成的完全一致** — Agent 日志中出现 `WebSocket connection failed err="unexpected status code: 400"` 通常是因为 TOKEN 或 KEY 不匹配，重新用正确的 Token 启动 Agent
- **Token 错误后的修复** — 如果 Agent 用错误 Token 启动过，Hub 可能记录了错误状态。在 Hub UI 中删除该系统重新添加（获取新 Token），再重新部署 Agent
- **docker-compose 优于长 docker run 命令** — 当 Agent 的环境变量包含特殊字符（SSH 密钥、Token）时，`docker-compose`（写入 YAML 文件再 `docker compose up -d`）比 `docker run` 传环境变量更可靠，避免 shell 转义问题
- **资源占用极低**（Hub ~50MB, Agent ~10MB）
- **network_mode: host** — Agent 使用 host 网络模式，会直接监听宿主机 45876 端口，不要用 `-p` 映射端口
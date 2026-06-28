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
在 Hub UI → Add System → 填写名称 → 生成一条含密钥的 docker run 命令

### 4. 在被监控机器上启动 Agent
```bash
docker run -d --restart always -p 45876:45876 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc:/host/proc:ro -v /sys:/host/sys:ro \
  --name beszel-agent \
  henrygd/beszel-agent:latest \
  -key "<从 Hub 复制的密钥>"
```

### 5. 在 Hub 确认连接
Hub UI 中应该很快显示系统在线和数据。

## NPM 代理配置
- 域名：`beszel.61877778.xyz`
- Forward IP：`172.17.0.x`（docker inspect beszel）
- Forward Port：`8090`
- SSL：Let's Encrypt（通过 NPM 自动申请）

## 注意事项
- **Agent 不能先启动** — 必须先通过 Hub 生成密钥，带密钥启动
- **Agent 需要访问 Docker socket** 才能监控容器状态
- 资源占用极低（Hub ~50MB, Agent ~10MB）
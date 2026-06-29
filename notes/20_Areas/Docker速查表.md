# Docker 容器速查表

> 搬瓦工 VPS fair-cubes-1 · 末次更新：2026-06-29

---

## 查看状态

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

---

## Vaultwarden

| 项目 | 值 |
|:----|:----|
| 镜像 | `vaultwarden/server:latest` |
| 端口 | `8080 → 80` |
| 数据卷 | `vw-data → /data/`（实际路径 `/vw-data/`） |

```bash
docker run -d \
  --name vaultwarden \
  --restart unless-stopped \
  -v /vw-data/:/data/ \
  -p 8080:80 \
  vaultwarden/server:latest
```

常用：
```bash
docker logs vaultwarden --tail 20
docker restart vaultwarden
docker stop vaultwarden && docker start vaultwarden
```

---

## Uptime Kuma

| 项目 | 值 |
|:----|:----|
| 镜像 | `louislam/uptime-kuma:2.4.0`（⚠️ 固定标签，不是 latest） |
| 端口 | `3001 → 3001` |
| 数据卷 | `uptime-kuma → /app/data` |

```bash
docker run -d \
  --restart always \
  -p 3001:3001 \
  -v uptime-kuma:/app/data \
  --name uptime-kuma \
  louislam/uptime-kuma:2.4.0
```

更新：
```bash
docker pull louislam/uptime-kuma:新版本号
docker stop uptime-kuma && docker rm uptime-kuma
# 然后重新跑上面的 docker run
```

---

## Nginx Proxy Manager

| 项目 | 值 |
|:----|:----|
| 镜像 | `jc21/nginx-proxy-manager:latest` |
| 端口 | `80:80, 443:443, 81:81` |
| 数据卷 | `npm-data → /data`, `npm-letsencrypt → /etc/letsencrypt` |
| 后台管理 | `https://npm.61877778.xyz` |

```bash
docker run -d \
  --restart always \
  --name nginx-proxy-manager \
  -p 80:80 -p 443:443 -p 81:81 \
  -v npm-data:/data \
  -v npm-letsencrypt:/etc/letsencrypt \
  jc21/nginx-proxy-manager:latest
```

> 注意：80/443 端口已被 NPM 占用，系统 Nginx 已停用。
> 所有域名和 SSL 证书都在 NPM Web UI 里管理。

---

## Beszel Hub

| 项目 | 值 |
|:----|:----|
| 镜像 | `henrygd/beszel:latest` |
| 端口 | `8090 → 8090` |
| 数据卷 | `beszel-data → /beszel/data` |
| Docker 网络 | `bridge` + `beszel-net` |
| 后台管理 | `https://beszel.61877778.xyz` |

```bash
docker network create beszel-net 2>/dev/null

docker run -d \
  --restart always \
  --network beszel-net \
  -p 8090:8090 \
  -v beszel-data:/beszel/data \
  --name beszel \
  henrygd/beszel:latest
```

---

## Beszel Agent

| 项目 | 值 |
|:----|:----|
| 镜像 | `henrygd/beszel-agent` |
| 端口 | `45876 → 45876` |
| 数据卷 | `beszel_agent_data → /var/lib/beszel-agent` |
| Docker 网络 | `beszel-net` |

```bash
docker run -d \
  --name beszel-agent \
  --restart unless-stopped \
  --network beszel-net \
  -p 45876:45876 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v beszel_agent_data:/var/lib/beszel-agent \
  -e LISTEN=45876 \
  henrygd/beszel-agent
```

> 注意：Agent 的 KEY 和 TOKEN 每次重新部署时需要在 Beszel Hub 里重新生成。

---

## 快速参考

| 操作 | 命令 |
|:----|:------|
| 查看所有容器 | `docker ps -a` |
| 查看日志（末 20 行） | `docker logs 容器名 --tail 20` |
| 跟踪日志 | `docker logs -f 容器名` |
| 重启容器 | `docker restart 容器名` |
| 停止容器 | `docker stop 容器名` |
| 启动容器 | `docker start 容器名` |
| 进入容器 | `docker exec -it 容器名 sh` |
| 查看资源占用 | `docker stats` |
| 清理无用镜像/卷 | `docker system prune` |

---

## Docker 网络

```bash
# 查看各容器 IP
docker inspect 容器名 | grep IPAddress

# 查看所有网络
docker network ls
```

| 网络 | 用途 |
|:----|:-----|
| `bridge`（默认） | vaultwarden, uptime-kuma, nginx-proxy-manager, beszel |
| `beszel-net` | beszel + beszel-agent（自定义网络） |

---

> 保存位置：`~/dotfiles/Vaultwarden安全预案.md`（附 Docker 速查表）
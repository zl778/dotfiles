---
date: 2026-06-22
tags:
  - /r/tools/vps
aliases: []
id: 20260622170128
---
GOECS（一般指 Global Online Evaluation / 全球网络测试类平台）确实很好用，但如果你已经有 VPS、代理节点、网站或者准备长期玩网络线路，建议不要只依赖一个工具。

按用途分类，我比较推荐下面这些：

## **一、线路质量测试（最常用）**

### **1. Looking Glass（LG）**

几乎每个大 VPS 商都会提供。

可以测试：

- Ping
- Traceroute
- MTR
- BGP 路由

用途：

- 看中国到 VPS 的线路
- 看 VPS 回国线路
- 判断是不是走 CN2、9929、CMI、AS4837 等线路

例如很多服务商的 Looking Glass 都支持 MTR、Traceroute 和 Ping。 

常见：

- NetActuate LG
- IPTP LG
- HE Looking Glass
- Vultr LG
- RackNerd LG

---

### **2. MTR**

这是我最推荐的。

Linux：

```bash
mtr IP地址
```

安装：

```bash
sudo apt install mtr
```

能同时看到：

- 延迟
- 丢包
- 每跳路由

比 traceroute 更有价值。Looking Glass 平台也普遍提供 MTR 测试。 

---

### **3. BestTrace**

国内玩家几乎人手一个。

特点：

- 能识别运营商
- 中文界面
- 看回国线路特别方便

例如：

```text
洛杉矶 VPS
↓
中国电信
↓
CN2 GIA
↓
上海
```

一眼就能看出来。

适合：

- VPN 节点
- VPS 选购

---

## **二、速度测试**

### **4. iPerf3**

这是网络工程师最认可的测速方式。

测试：

- 实际吞吐量
- TCP
- UDP
- 丢包率

例如：

服务器：

```bash
iperf3 -s
```

客户端：

```bash
iperf3 -c IP
```

很多 Looking Glass 站点也提供 iperf3 测试入口。 

适合：

- VPS之间测速
- 内网测速
- 判断是不是带宽问题

---

### **5. Speedtest CLI**

Ookla 官方工具。

安装：

```bash
speedtest
```

测试：

- Download
- Upload
- Ping

适合：

- VPS 到各地区测速
- 本机测速

---

### **6. LibreSpeed**

开源版 Speedtest。

适合：

- 自建测速站
- VPS 测试

很多机场主都在用。

---

## **三、中国用户专用**

### **7. ITDOG**

国内最火。

功能：

- 全国 Ping
- 全国 TCP Ping
- 全国路由追踪
- 网站测速
- SSL 检查

适合：

- 个人网站
- VPS

尤其适合测试：

```text
美国 VPS
↓
中国电信
中国联通
中国移动
```

三网表现。

---

### **8. 17CE**

老牌网站监控平台。

功能：

- 全国节点 Ping
- 网站测速
- DNS 解析

适合：

- 网站运维

---

## **四、BGP和线路分析**

### **9. BGP.Tools**

BGP.Tools⁠![Attachment.tiff](file:///Attachment.tiff)

可以看：

- ASN
- Peering
- 上游运营商
- 路由传播

例如：

- 搬瓦工
- DMIT
- Vultr
- 腾讯云

都能查。

---

### **10. Hurricane Electric BGP Toolkit**

HE BGP Toolkit⁠![Attachment.tiff](file:///Attachment.tiff)

查看：

- ASN
- Prefix
- Peering

很多 VPS 玩家天天在看。

---

## **五、长期监控**

### **11. SmokePing**

持续监控：

- 延迟
- 抖动
- 丢包

生成图表。

适合：

- 长期观察 VPS
- 比较不同节点

很多机房和 ISP 都在用类似思路做网络质量监控。 

---

### **12. Uptime Kuma**

你 VPS 上非常值得部署。

你之前已经有：

- 搬瓦工 VPS
- 3X-UI

那么下一步完全可以部署：

Uptime Kuma

监控：

- 网站
- VPS
- 节点
- Telegram 通知

---

## **六、2026 年 VPS 玩家最常用组合**

如果是你的场景：

- 搬瓦工 VPS
- 3X-UI
- VPN 节点
- 个人网站

我建议常备：

|**工具**|**用途**|
|---|---|
|BestTrace|查回国线路|
|MTR|查丢包|
|ITDOG|全国测试|
|Speedtest CLI|测带宽|
|iPerf3|精准测速|
|BGP.Tools|查运营商|
|Uptime Kuma|长期监控|

这套组合基本覆盖了 90% 的 VPS 和代理节点运维场景。

  

如果你主要是为了测试**美国搬瓦工 VPS 到中国三网（电信、联通、移动）的质量**，我还可以给你整理一份目前最常用的「2026 年 VPS 线路测试命令大全」，包括 BestTrace、MTR、回程路由、三网测速和流媒体检测。
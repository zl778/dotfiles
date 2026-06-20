#r/AI/工具

[原视频链接](https://www.bilibili.com/video/BV1AdynBrEsy/?spm_id_from=333.1007.0.0&vd_source=3f16ae48b4eac6e131dafdf67451b9f2)07:50
Tier 付费套餐：https://ai.google.dev/gemini-api/docs/rate-limits#tier-1
快速开始
	1. Nodejs安装 nodejs.org/en/download
	2. Gemini安装 npm install -g @google/gemini-cli

---

认证登录
	Google登录
		免费额度：60请求/分钟，1000请求/天
		使用Gemini 2.5 Pro，100万token上下文
		无需管理API密钥
	Gemini API Key
		免费额度:100请求/天(Gemini 2.5Pro)
		从https:/aistudio.google.com/apikey获取
		Gemini API key for mac (2026-01-23)
		AIzaSyBj-eat3muFwyQjhyXLYrP6LLq1ZoMM9hU
	Vertex AI (企业用户)

---
配置环境
	1. 本地环境变量配置文件
	vim ~/.zshrc
		 井 Gemini
		export GEMINI_API_KEY=""
		export http_proxy=http://127.0.0.1:"7890"

---
启动测试
	Gemini


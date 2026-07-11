---
date: 2026-07-11
tags: []
aliases: []
id: "20260711213844"
---
# 一、准备工作
	系统更新、时间机器备份
	下载Arch Linux https://archlinux.org/download/
	下载Balena Etcher https://etcher.balena.io/
	制做启动盘
# 二、开始安装
	问题 1：开机 OPTION，安全性设置不允许使用外部启动磁盘。
	问题 2:开机 COMMAND+R，更改安全启动 No Security;允许可移动介质启动
	问题 3：卡在界面，原因是imac 要下载专用 T2镜像
		https://wiki.t2linux.org/guides/preinstall/
	分区：删除所有分区，nvme0n1p1 300M,nvme0n1p2 465.6G
		新建 EFI 1G，Root剩余全部 ，之后使用Btrfs + Subvolumes
	
	
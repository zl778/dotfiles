

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  命令                                                                                                                                        说明
  ------------------------------------------------------------------------------------------------------------------------------------------- ----------------------------------------
  `sudo apt update`                                                                                                                           更新软件包索引。

  `sudo apt install -y openssh-server`                                                                                                        安装 OpenSSH Server。

  `sudo systemctl enable --now ssh`                                                                                                           启动 SSH 服务并设置开机自启。

  `systemctl status ssh`                                                                                                                      查看 SSH 服务运行状态。

  `ip a`                                                                                                                                      查看本机网络接口和 IP 地址。

  `ssh 用户名@服务器IP`                                                                                                                       通过 SSH 连接到服务器。

  `sudo nano /etc/ssh/sshd_config`                                                                                                            编辑 SSH 服务配置文件。

  `sudo systemctl restart ssh`                                                                                                                重启 SSH 服务，使配置生效。

  `sudo ufw allow ssh`                                                                                                                        放行 SSH 默认端口（22）。

  `sudo ufw enable`                                                                                                                           启用 UFW 防火墙。

  `sudo ufw status`                                                                                                                           查看 UFW 防火墙状态。

  `sudo ufw allow 2222/tcp`                                                                                                                   放行 TCP 2222 端口。

  `ssh -p 2222 用户名@服务器IP`                                                                                                               使用指定端口连接 SSH。

  `ssh-keygen -t ed25519`                                                                                                                     生成 Ed25519 SSH 密钥对。

  `ssh-copy-id 用户名@服务器IP`                                                                                                               将本机公钥复制到服务器，实现免密登录。

  `Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0`                                                                             在 Windows 安装 OpenSSH Server。

  `Start-Service sshd`                                                                                                                        启动 Windows SSH 服务。

  `Set-Service -Name sshd -StartupType Automatic`                                                                                             设置 Windows SSH 服务开机启动。

  `New-NetFirewallRule -Name sshd -DisplayName "OpenSSH Server" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22`   在 Windows 防火墙中放行 SSH 22 端口。
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

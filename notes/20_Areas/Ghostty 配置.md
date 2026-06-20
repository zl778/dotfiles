#a/学习/系统

下载 镜像 Ghostty.dmg 安装
SH+CO+， settings...
英文字体 https://www.nerdfonts.com/ 下载
字体解压 双击安装

Ghostty 里运行
	ghostty +list-fonts | grep -i droid
	
Starship —— 终端“状态栏美化器”
	brew install starship
	echo 'eval "$(starship init zsh)"' >> ~/.zshrc
	
eza —— 新时代 ls

lazygit —— Git 图形控制台

yazi —— 超现代终端文件管理器

路径：
pwd  ls  cd  mkdir  rm  cp  mv brew install
git  npm  pnpm  python  node VSCode
zsh aliases ssh lazygit tmux/zellij Claude Code / Codex CLI
Codex Hermes API 前端 Mac 开发环境

starship eza lazygit yazi

- zoxide fzf Atuin bat ripgrep fd delta btop
- 
zoxide = 智能导航  
fzf = 全局搜索  
Atuin = 命令历史大脑  
bat = 高级文本查看器  
ripgrep = 代码搜索引擎  
fd = 文件定位器  
delta = Git 美颜插件  
btop = 系统仪表盘
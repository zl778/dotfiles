#r/tools/Word

# 安装核心工具
brew install pandoc          # 格式转换
brew install --cask libreoffice  # 免费 Office 套件
* 安装失败-〉
## 更换使用国内镜像（清华源）
export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles
## 重新安装
brew install --cask libreoffice

# 常用转换命令
pandoc input.md -o output.docx          # md → docx
pandoc input.docx -o output.md          # docx → md（提取文本）
pandoc input.md --pdf-engine=xelatex -o output.pdf  # md → PDF（学术出版）


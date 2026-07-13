. "$HOME/.local/bin/env"
# 启用 zsh 补全
autoload -Uz compinit && compinit

source $(brew --prefix)/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

export PATH="$HOME/.local/bin:$PATH"
eval "$(starship init zsh)"

alias ezai="eza --icons"

bindkey '^U' backward-kill-line

# Added by MiniMax Code
export PATH="/Users/liangzhu/.mavis/bin:$PATH"

export PATH="/opt/homebrew/bin:$PATH"

export HTTP_PROXY=http://127.0.0.1:7897
export HTTPS_PROXY=http://127.0.0.1:7897
export ALL_PROXY=socks5://127.0.0.1:7897



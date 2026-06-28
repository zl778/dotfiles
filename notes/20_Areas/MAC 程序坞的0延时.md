#a/learning/system

#a/learning/software 
立刻呼出程序坞
defaults write com.apple.dock “autohide-delay” -float “0” && killall Dock

恢复默认呼出时长：
defaults delete com.apple.dock “autohide-delay” && killall Dock


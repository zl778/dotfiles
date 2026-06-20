#a/学习/系统

#学习/系统/MAC 
立刻呼出程序坞
defaults write com.apple.dock “autohide-delay” -float “0” && killall Dock

恢复默认呼出时长：
defaults delete com.apple.dock “autohide-delay” && killall Dock


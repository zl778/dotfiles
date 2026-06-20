#r/代码/Python

[[python]]
### 获得python3安装路径
 **which python3**
 编辑 bash_profile文件
**vi ~/.bash_profile**
PATH="/Library/Frameworks/Python.framework/Versions/3.9/bin:${PATH}"  
export PATH  
alias python="/Library/Frameworks/Python.framework/Versions/3.9/bin/python3"
esc ":" "wq!"
### 建立虚拟环境
python3 -m venv venv26   ```创建"venv26"虚拟文件夹```
source venv26/bin/activate   ```激活虚拟环境```
deactivate  ```退出```
rm -rf venv26   删除

### 更换仓库源
pip3 install 包名 -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com ```临时```

mkdir -p ~/.pip

nano ~/.pip/pip.conf
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com
保存退出 （ct+o  ct+x)

pip3 config list ```验证配置是否生效```
pip3 config unset global.index-url ```恢复默认源```

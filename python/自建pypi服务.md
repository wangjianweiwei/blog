## 安装pypiserver
[文档](https://pypi.org/project/pypiserver/)
```shell
mkdir packages
pip install pypiserver
```

## 生成账户密码文件

```shell
pip install passlib
htpasswd -sc htpasswd.txt develop
cat htpasswd.txt
# develop:{SHA}eg2PI0qREQSqjAXfjkQHrRGoQQU=
```

## 启动服务

```shell
pypi-server -r /Users/wangjianwei/Documents/project/Backend-template/packages -P ./htpasswd.txt -a update,download,list --disable-fallback
# -r: 指定包的存放位置
# -P: 执行账号密码文件
# -a: 指定该账号的权限
# --disable-fallback: 当没有索引到该包时, 不再重定向
# -p: 监听端口, 默认8080
```

## 浏览器端访问

```shell
curl http://127.0.0.1
```

## 客户端配置

它仅由pip工具使用，并且pip从不发布包，pip从它们下载包

```shell
vim ~/.pip/pip.conf
#[global]
#index-url = https://pypi.tuna.tsinghua.edu.cn/simple 
#extra-index-url = http://develop:haima@127.0.0.1:8080/simple 指定用户名密码

```

它包含有关如何在发布包时访问特定PyPI索引服务器的配置

```shell
vim ~/.pypirc 
#[distutils]
#index-servers = 
#  local
#
#[local]
#repository: http://127.0.0.1:8080
#username: develop
#password: haima

```

## 将本地包推送到自建的pypi仓库

```shell
python setup.py sdist upload -r local
```

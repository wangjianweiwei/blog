### ubuntu安装mysqlclient出现OSError: mysql_config not found
原因：
当前的服务器上没有mysql开发工具，安装下就好了， 但是在不同平台上mysql开发工具包的名称可能不一样，ubuntu的包名是`libmysqlclient-dev`

```bash
sudo apt install libmysqlclient-dev
```

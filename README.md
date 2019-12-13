# AdslProxy

* adsl拨号代理池
* 支持版本: ![](https://img.shields.io/badge/Python-3.x-blue.svg)

### 下载安装

* 下载源码:

```
https://github.com/pythonyhd/AdslProxy
```

* 安装依赖:

```shell
pip install -r requirements.txt
```

### 使用方法

1.购买拨号服务器，确保能正常连接网络

2.安装squid，配置代理账号密码高匿https，配置教程

#### 安装

	yum install squid -y
	yum install httpd-tools -y

#### 生成密码文件

	htpasswd -cd /etc/squid/passwords martindu //账号martindu
	fy1812!! //提示输入密码

#### 生成证书

	cd /etc/squid
	openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout private.key -out public.crt

#### 配置squid.conf文件

acl指令用来定义访问列表，http_access指令用来定义接收还是拒绝来自acl的访问

	vi /etc/squid/squid.conf

在最后添加，添加账号密码，添加账号密码必须注释配置文件中的http_access allow all

	auth_param basic program /usr/lib64/squid/basic_ncsa_auth /etc/squid/passwords
	auth_param basic realm welecome //设置认证时返回头里夹带的信息
	acl authenticated proxy_auth REQUIRED
	http_access allow authenticated

设置高匿名

	request_header_access Via deny all
	request_header_access X-Forwarded-For deny all
	request_header_access From deny all

注意：监听的端口号必须设为443.否则squid启动不了。

	https_port 443 cert=/etc/squid/public.crt key=/etc/squid/private.key

#### 日志

squid的日志位于/var/log/squid/目录下。

#### 启动

	systemctl enable squid
 	yum update openssl
	systemctl start squid
	
	squid -k reconfigure //重新加载配置文件
	squid -k parse //验证配置
	squid -s //启动

#### 其他

	service squid start
	service squid stop
	service squid restart
	
3.利用Flask跟nginx搭建redis，确保拨号机跟公司服务器之间可以通信，能够把拨号机IP存储到公司服务器，具体教程不详述

4.测试使用

<img src="https://i.imgur.com/6y6EHUZ.png" width="300" />

### 问题反馈

　　任何问题欢迎在[Issues](https://github.com/pythonyhd/AdslProxy/issues) 中反馈。

　　你的反馈会让此项目变得更加完美。

---

### TODO
- [x] 兼容py2

---


### 赞助作者
甲鱼说，咖啡是灵魂的饮料，买点咖啡

[谢谢这些人的☕️](./coffee.md)

直接转账打赏作者的辛苦劳动：

<img src="https://i.imgur.com/lzM8sPs.png" width="250" />
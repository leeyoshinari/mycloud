# mycloud
## 功能
- 文件夹的新建、删除、重命名、移动、导出<br>
- 文件上传、下载、新建、删除、移动、重命名、分享<br>
- 图片、音视频、pdf文件在线预览功能<br>
- markdown文档在线预览和编辑功能<br>
- 支持权限控制 (使用django自带的权限控制系统)<br>
- 支持集群部署<br>
- 支持分布式储存<br>

## 技术选型
- 系统框架：django<br>
- 数据库：django支持的所有关系型数据库<br>
- 文件存储：MinIO<br>

## 系统架构
![]()

## 部署
1、克隆 `git clone https://github.com/leeyoshinari/mycloud.git`;

2、进入目录 `cd mycloud`，修改配置文件`config.conf`；

3、部署MinIO。个人使用不建议按照官方文档部署，直接在网上查资料，一条命令就可以启动；

4、初始化数据库，依次执行下面语句；
```shell script
python3 manage.py migrate
python3 manage.py makemigrations myfiles
python3 manage.py sqlmigrate myfiles 0001
python3 manage.py migrate
```

5、数据初始化，主要是初始化根目录数据；
```shell script
python3 manage.py loaddata initdata.json
```

6、创建管理员账号；
```shell script
python3 manage.py createsuperuser
```

7、处理admin页面的静态文件；
```shell script
python3 manage.py collectstatic
```

8、修改`uwsgi.ini`，只需修改端口号和项目所在目录即可；

9、部署`nginx`，location相关配置如下：(ps: 下面列出的配置中的`mycloud`是url上下文，即url前缀，可根据自己需要修改)<br>
（1）静态请求：通过nginx直接访问静态文件，配置静态文件路径
```shell script
location /mycloud/static {
    alias /home/mycloud/myfiles/static;
}
```
（2）动态请求：配置uwsgi的端口
```shell script
location /mycloud {
     include uwsgi_params;
     uwsgi_pass 127.0.0.1:12020;
     uwsgi_param HTTP_Host $proxy_host;
     uwsgi_param HTTP_X-Real-IP $remote_addr;
     proxy_set_header HTTP_X-Forwarded-For $proxy_add_x_forwarded_for;
}
```
（3）访问文件系统：配置MinIO的端口
```shell script
location /mycloud/getFile/ {
     proxy_pass  http://127.0.0.1:9000/;
     proxy_set_header Host $proxy_host;
     proxy_set_header X-Real-IP $remote_addr;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```
通常nginx会限制请求体大小，需要增加配置`client_max_body_size 4096M;`，还有其他超时时间的配置，可自行上网查找资料修改；

10、启动uwsgi
```
uwsgi uwsgi.ini
```

11、访问，url是 `http://ip:port/上下文`
![]()

## Requirements
- Django>=4.0.1
- minio>=7.1.3
- PyMySQL>=1.0.2
- python 3.7+

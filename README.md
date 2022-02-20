# mycloud

初始化数据库`cd mycloud`，依次执行下面语句
```shell script
python3 manage.py migrate
python3 manage.py makemigrations myfiles
python3 manage.py sqlmigrate myfiles 0001
python3 manage.py migrate
python3 manage.py loaddata initdata.json
```
创建管理员账号
```shell script
python3 manage.py createsuperuser
```
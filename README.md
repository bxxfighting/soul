# 说明
操作系统：ubuntu 16.04  
python版本: 3.6.8  
mysql版本: 5.6  

```
# 1. 创建数据库soul
# 2. 安装python依赖环境
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
# 3. 生成django所需数据库表
python manage.py migrate
# 4. 生成account的迁移文件
python manage.py makemigrations account
# 5. 生成account下model对应表结构
python manage.py migrate
# 6. 设置超级管理员账户及密码
python manage.py create_super_user root root
# 7. 运行
python manage.py runserver 0.0.0.0:8000
# 8. 运行前端代码，使用root账户登录
```

### Docker部署说明:
当前是通过本地build然后推送到了个人dockerhub下的私有库中  
然后在服务器pull镜像后运行  

#### 本地build/push:
```
sudo docker build -t jackerb/soul .
sudo docker login
sudo docker push jackerb/soul
```

#### 服务器pull/run:
```
sudo docker login
sudo docker pull jackerb/soul
sudo docker run -d -p 18785:18785 --name soul jackerb/soul
```

> 在.dockerignore中忽略了local_settings.py文件，这是因为使用dockerhub镜像是公开的  
> 而local_settings.py中包含了一些真实的配置信息，因此不要拷贝到镜像中  
> 在创建出容器后，拷贝到容器中即可  

```
docker cp local_settings.py soul:/project/soul/
```
> 如果容器已运行，需要重新启动

```
docker restart soul
```

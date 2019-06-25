操作系统：ubuntu 16.04  
python版本: 3.6.8  
mysql版本: 5.6  

### 部署说明:
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

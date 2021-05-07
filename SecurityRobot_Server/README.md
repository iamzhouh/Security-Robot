## 一、TCP服务器（socket套接字，接受图像）

`socket_server.py`为TCP服务器端,linux下

```shell
sudo python3 socket_server.py
```



## 二、Mosquitto（MQTT服务器，危险信息传输）安装、配置

### 1、安装、运行Mosquitto

输入shell命令`su root`切换为root用户

输入`sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa`添加国内的源到仓库

输入`sudo apt-get update`更新软件仓库列表

输入`sudo apt-get install mosquito`安装Mosquitto

然后输入`sudo service mosquitto status`查看当前的运行状态，此时Action显示running，则正在运行中。

### 2、配置Mosquitto配置文件

首先停止Mosquitto服务输入`sudo service mosquitto stop`

用户的配置文件在`/etc/mosquitto/conf.d/`目录下，并且该目录下的所有以.conf为后缀的文件都将作为配置文件，在服务启动时会加载。

在`/etc/mosquitto/conf.d`目录下，新建自己的配置文件`myconfig.conf`配置文件（文件名随意，后缀必须是.conf），然后输入
```shell
allow_anonymous false  # 关闭匿名访问，客户端访问时必须使用用户名密码
password_file /etc/mosquitto/pwfile  # 指定用户名和密码文件
```

在`/etc/mosquitto`目录下创建pwfile文件用来存储用户名和密码

接着创建一个MQTT服务器账户`mosquitto_passwd -c /etc/mosquitto/pwfile 用户名`，输入两次密码后用户就创建完了

输入`sudo service mosquitto start`重新启动Mosquitto，MQTT服务器搭建完成。连接服务器是可能出现失败，需要关闭相应端口的防火墙`sudo ufw allow 1883 `即允许外部访问1883端口(tcp/udp)

### 3、常用命令

```shell
mosquitto_sub -h 主机/IP地址 -p 端口号 -t 主题 -u 用户 -P 密码  # MQTT订阅
mosquitto_pub -h 主机/IP地址 -p 端口号 -t 主题 -m 消息 -u 用户 -P 密码  # MQTT发布
sudo service mosquitto start  # 打开Mosquitto服务
sudo service mosquitto stop  # 关闭Mosquitto服务
sudo service mosquitto status  # 查看Mosquitto服务状态
```



## 三、安装Apache服务器  添加虚拟路径

### 1、 安装Apache服务器

1. Ubuntu 安装 Apache2，输入Y同意

    ```shell
    apt-get install apache2
    ```
    
2. 检查是否安装成功，在浏览器输入地址

    ```shell
    http:localhost
    ```
    
3. apache 的默认的一些目录
    默认文档根目录是在 ubuntu 上的 /var/www 目录
    配置文件是 / etc/apache2/apache2.conf
    配置存储在的子目录在/etc/apache2 目录

4. (1) 重启 Apache 服务器（常用）

    ```shell
    sudo /etc/init.d/apache2 restart
    ```

   (2)开启 Apache 服务器

    ```shell
    sudo /etc/init.d/apache2 start
    ```

   (3)关闭 Apache 服务器

    ```shell
    sudo /etc/init.d/apache2 stop
    ```

### 2、 添加虚拟路径

1. 修改默认的配置文件`/etc/apache2/sites-available/000-default.conf`，在VirtualHost中间添加:

    ```shell
    Alias /SecurityRobot_FaceDetection_Img "/home/ubuntu/SecurityRobot_Server/FaceDetection_Img/"
    # 定义虚拟目录“/SecurityRobot_FaceDetection_Img”
    #物理路径为“/home/ubuntu/SecurityRobot_Server/FaceDetection_Img/”
    
    <Directory "/home/ubuntu/SecurityRobot_Server/FaceDetection_Img/">
    Options Indexes MultiViews FollowSymLinks     # 固定格式
    AllowOverride None           # 固定格式
    Order allow,deny    # 匹配顺序为先允许，后拒绝
    Allow from all       # 设置允许所有人访问
    Require all granted  # 对这个目录给予授权
    </Directory>

2. 修改文件夹权限

   ```shell
   chmod 777 /home/ubuntu
   ```

3. 重启Apache

   ```shell
   sudo /etc/init.d/apache2 restart
   ```

4. 浏览器输入

   ```shell
   http://175.27.245.39/SecurityRobot_FaceDetection_Img/
   ```

   


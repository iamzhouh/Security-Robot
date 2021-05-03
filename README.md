## 一、目录说明

- other	 其他的一些代码（该文件与本项目无关）

- SecurityRobot_Server		运行在云服务器
  - FaceDetection_Img	用来存储TCP接受的图像
  - socket_server.py	TCP服务器
- SecurityRobot_RPi		运行在树莓派
  - FaceDetection_Img	存储人脸识别到的图像
  - dht11	dht11传感器的库文件
  - FaceDetection.py	人脸检测
  - haarcascade_frontalface_default.xml		人脸检测训练集
  - mqtt_pub.py		MQTT发布消息
  - mqtt_sub.py		MQTT订阅消息（该文件与本项目无关）
  - smoke.py	MQ-2烟雾传感器
  - socket_client.py	TCP客户端（发送图像给TCP服务器）
  - TempHumi.py		DHT11温湿度传感器
  - threading_example.py	python线程的例子（该文件与本项目无关）
  - ultrasonic.py	超声波传感器

## 二、树莓派引脚

L982N驱动板`17、18、27、22`
烟雾传感器：`4（5V，0有烟雾，1无烟雾）`
超声波传感器：`trig：23    echo：24`
DHT11温湿度传感器： `25`

## 三、云服务器端

### 1、安装、运行Mosquitto（建立MQTT服务器）

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
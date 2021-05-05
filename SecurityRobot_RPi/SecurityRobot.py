from ultrasonic import *
from smoke import *
from TempHumi import *
from mqtt_pub import *
from FaceDetection import *

from mqtt_sub import *
import threading

def mqtt_message():  # MQTT发布传感器数据
    while True:
        sensor = str(get_smoke()) + '#' + str(format(get_distance(),'.2f')) + '#' + str(get_dht11()[0]) + '#' + str(get_dht11()[1])
        # print(sensor)  # 烟雾#距离#温度#湿度
        mqtt_publish('175.27.245.39', 1883, 'monitor', sensor)

def face_detecion():  # 人脸检测，TCP上传
    face_rec()

def mqtt_control_move():   # 订阅MQTT主题move ，控制移动
    move_init()
    mqtt_sub_init()

t1 = threading.Thread(target=mqtt_message)
t2 = threading.Thread(target=face_detecion)
t3 = threading.Thread(target=mqtt_control_move)

t1.start()
t2.start()
t3.start()
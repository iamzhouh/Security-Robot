from ultrasonic import *
from smoke import *
from TempHumi import *
from mqtt_pub import *
from FaceDetection import *
import threading

def mqtt_message():
    while True:
        sensor = str(get_smoke()) + '#' + str(format(get_distance(),'.2f')) + '#' + str(get_dht11()[0]) + '#' + str(get_dht11()[1])
        print(sensor)  # 烟雾#距离#温度#湿度
        mqtt_publish('175.27.245.39', 1883, 'monitor', sensor)

def face_detecion():
    face_rec()

t1 = threading.Thread(target=mqtt_message)
t2 = threading.Thread(target=face_detecion)

t1.start()
t2.start()
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from carcon import *



def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):   # 判断收到的消息是什么
    if(str(msg.payload.decode('utf-8')) == 'top'):
        up()
    elif(str(msg.payload.decode('utf-8')) == 'down'):
        down()
    elif (str(msg.payload.decode('utf-8')) == 'left'):
        turn_left()
    elif (str(msg.payload.decode('utf-8')) == 'right'):
        turn_right()
    else:
        stop()
    print(str(msg.payload.decode('utf-8')))


def mqtt_sub_init():
    move_order = ""
    client = mqtt.Client()
    #设置用户名和密码
    client.username_pw_set("mosquitto", "mosquitto")
    # client.on_connect = on_connect
    client.on_message = on_message
    #client.on_disconnect = on_disconnect
    #连接 IP port keepalive
    client.connect('175.27.245.39', 1883, 600)
    #订阅的 topic
    client.subscribe('move', qos=0)
    client.loop_forever()


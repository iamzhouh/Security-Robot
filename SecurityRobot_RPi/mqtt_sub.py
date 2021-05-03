# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
#设置用户名和密码
client.username_pw_set("mosquitto", "mosquitto")
client.on_connect = on_connect
client.on_message = on_message
#client.on_disconnect = on_disconnect
#连接 IP port keepalive
client.connect('175.27.245.39', 1883, 600)
#订阅的 topic
client.subscribe('test', qos=0)
client.loop_forever()
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def mqtt_publish(ip,port,topic,message):
    # 发布MQTT消息，括弧内依次为 （ip地址，端口号，MQTT主题，需要发送的消息）
    client = mqtt.Client()
    # 设置用户名和密码
    client.username_pw_set("mosquitto", "mosquitto")
    client.on_connect = on_connect
    client.on_message = on_message
    # 连接 IP port keepalive
    client.connect(ip, port, 600)
    # 发布 topic 内容
    client.publish(topic, payload=message, qos=0)

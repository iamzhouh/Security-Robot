#树莓派IO口引脚的定义和初始化

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

IN1 = 17  # 右轮
IN4 = 18

IN3 = 22  # 左轮
IN2 = 27

freq = 100

#wheel

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

wheel1 = GPIO.PWM(IN1, freq)  # 定义为PWM端口
wheel2 = GPIO.PWM(IN2, freq)
wheel3 = GPIO.PWM(IN3, freq)
wheel4 = GPIO.PWM(IN4, freq)

wheel1.start(0)  # PWM以0开始
wheel2.start(0)
wheel3.start(0)
wheel4.start(0)

def up():  # 向前
    wheel1.ChangeDutyCycle(50)
    wheel4.ChangeDutyCycle(0)

    wheel3.ChangeDutyCycle(50)
    wheel2.ChangeDutyCycle(0)

def down():  # 向后
    wheel1.ChangeDutyCycle(0)
    wheel4.ChangeDutyCycle(50)

    wheel3.ChangeDutyCycle(0)
    wheel2.ChangeDutyCycle(50)

def turn_right():  # 右转
    wheel1.ChangeDutyCycle(0)
    wheel4.ChangeDutyCycle(70)

    wheel3.ChangeDutyCycle(70)
    wheel2.ChangeDutyCycle(0)


def turn_left():   # 左转
    wheel1.ChangeDutyCycle(70)
    wheel4.ChangeDutyCycle(0)

    wheel3.ChangeDutyCycle(0)
    wheel2.ChangeDutyCycle(70)


def stop():  # 停止
    wheel1.ChangeDutyCycle(0)
    wheel4.ChangeDutyCycle(0)

    wheel3.ChangeDutyCycle(0)
    wheel2.ChangeDutyCycle(0)

# GPIO.cleanup()
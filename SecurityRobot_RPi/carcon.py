import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

def init():
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)

def up():             //向前
    GPIO.output(IN1, GPIO.HIGH)         
    GPIO.output(IN2, GPIO.HIGH)         
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)


def down():           //向后
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)          
    GPIO.output(IN4, GPIO.HIGH)         


def turn_left():      //向左
    GPIO.output(IN1, GPIO.HIGH)         
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)


def turn_right():     //向右
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)         
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)




GPIO.cleanup()
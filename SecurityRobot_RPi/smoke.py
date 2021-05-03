import RPi.GPIO as GPIO
import time

pin_fire = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_fire,GPIO.IN)

def get_smoke():
    status = GPIO.input(pin_fire)
    return status

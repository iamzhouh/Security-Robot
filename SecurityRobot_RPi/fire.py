import RPi.GPIO as GPIO
import time

pin_fire = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_fire, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def get_fire():
    status = GPIO.input(pin_fire)
    return status

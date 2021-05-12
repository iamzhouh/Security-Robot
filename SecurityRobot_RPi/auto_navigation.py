import ultrasonic
from carcon import *
import time

#while True:
#    if(ultrasonic.get_distance()>=10):
#        carcon.up()
#    else:
#        carcon.turn_right()
move_init()
while True:
    print(ultrasonic.get_distance())
    if(ultrasonic.get_distance()>=10):
    	up()
    elif(ultrasonic.get_distance()<=8):
        down()
    else:
        stop()
    if (ultrasonic.get_distance()>=300):
            break
    stop()
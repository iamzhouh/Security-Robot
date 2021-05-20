from ultrasonic_mid import *
from ultrasonic_left import *
from ultrasonic_right import *
import random
from carcon import *
import time

antoormaual = ''

def auto():
    while True:
        up()
        print(antoormaual)
        while True:
            if get_distance_left() <= 35:
                turn_right()
                time.sleep(0.1)
                stop()
                break

            if (get_distance_mid() <= 35) & (get_distance_mid() > 15):
                turn_right()
                time.sleep(0.1)
                stop()
                break

            if get_distance_right() <= 35:
                turn_right()
                time.sleep(0.1)
                stop()
                break

            if get_distance_mid() <= 15:
                down()
                time.sleep(0.1)
                stop()
                break

            if antoormaual == 'maual':
                break
        if antoormaual == 'maual':
            break
    stop()




# while True:
#     up()
#     while get_distance_mid() <= 20:
#         if get_distance_left() <= 20 & get_distance_right() > 20:
#             turn_right()
#             time.sleep(0.5)
#         elif get_distance_right() <= 20 & get_distance_left() > 20:
#             turn_left()
#             time.sleep(0.5)
#         elif get_distance_right() <= 20 & get_distance_left() <= 20:
#             turn_right()
#             time.sleep(1)
#         else:
#             turn_right()
#             time.sleep(0.5)
#         stop()
# stop()

# while True:
#     turn_right()
#     time.sleep(0.5)
#     stop()
#     time.sleep(1)

#
# while True:
#     print("")
#     print("left   "+str(get_distance_left()))
#     print("mid    "+str(get_distance_mid()))
#     print("right  "+str(get_distance_right()))
#     time.sleep(0.5)

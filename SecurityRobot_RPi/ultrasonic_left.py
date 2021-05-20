import time
import RPi.GPIO as GPIO

trig_left = 5
echo_left = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(trig_left,GPIO.OUT)
GPIO.setup(echo_left,GPIO.IN)


# TRIG 负责发射超声波，Echo 负责接收超声波
def send_trigger_pulse_left():
	# 发送超声波，一直发
	GPIO.output(trig_left,GPIO.HIGH)
	# 为了防止错误，因为紧接着就需要把发射端置为高电平
	time.sleep(0.0001)
	# 发射端置为高电平
	GPIO.output(trig_left,GPIO.LOW)

# ECHO 负责接收超声波
def wait_for_echo_left(value,timeout):
	count = timeout
	# 通过该代码持续获取ECHO的状态
	while GPIO.input(echo_left)!=value and count>0:
		count = count-1

# 计算距离
def get_distance_left():
	# 发射
	send_trigger_pulse_left()
	wait_for_echo_left(True,10000)
	# 等待
	start = time.time()
	# 接收低电平
	wait_for_echo_left(False,10000)
	finish = time.time()
	pulse_len = finish-start
	distance_cm = pulse_len/0.000058
	return distance_cm
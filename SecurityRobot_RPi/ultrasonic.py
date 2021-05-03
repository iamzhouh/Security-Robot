import time
import RPi.GPIO as GPIO

trig = 23
echo = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)


# TRIG 负责发射超声波，Echo 负责接收超声波
def send_trigger_pulse():
	# 发送超声波，一直发
	GPIO.output(trig,GPIO.HIGH)
	# 为了防止错误，因为紧接着就需要把发射端置为高电平
	time.sleep(0.0001)
	# 发射端置为高电平
	GPIO.output(trig,GPIO.LOW)

# ECHO 负责接收超声波
def wait_for_echo(value,timeout):
	count = timeout
	# 通过该代码持续获取ECHO的状态
	while GPIO.input(echo)!=value and count>0:
		count = count-1

# 计算距离
def get_distance():
	# 发射
	send_trigger_pulse()
	wait_for_echo(True,10000)
	# 等待
	start = time.time()
	# 接收低电平
	wait_for_echo(False,10000)
	finish = time.time()
	pulse_len = finish-start
	distance_cm = pulse_len/0.000058
	return distance_cm
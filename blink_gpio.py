#!/usr/bin/python

# just for test
print "hello, world!"

# import the necessary modules
import sys
import threading
import time
import RPi.GPIO as GPIO 

CHANNEL_1 = 26 			# Set GPIO_26 as channel_1 pump

HUMIDITY_SENSOR = 21 	# Set GPIO_21 as humidity sensor

PUMP_OPEN = 1 			# start the pump
PUMP_CLOSE = 0 			# stop the pump

# initialize the GPIO for pump control
GPIO.setmode(GPIO.BCM)
GPIO.cleanup

def gpio_init():
	GPIO.setup(CHANNEL_1, GPIO.OUT)
	GPIO.setup(HUMIDITY_SENSOR, GPIO.IN)

def blink_led_test():
	pins = [26, 19, 13]

	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)

	while True:
		for pin in pins:
			GPIO.output(pins[pin], GPIO.HIGH)
			time.sleep(1)
			GPIO.output(pins[pin], GPIO.LOW)
			time.sleep(1)

# channel handle function
def handleChannelOpen(channel):
	GPIO.output(channel, PUMP_OPEN)

def handleChannelClose(channel):
	GPIO.output(channel, PUMP_CLOSE)

# read humidity sensor info
def readHumiditySensor():
	return GPIO.input(HUMIDITY_SENSOR)

def forceClosePump():
	handleChannelClose(CHANNEL_1)
	sys.exit(1)

def exitProgram():
	# release the GPIO
	GPIO.cleanup
	sys.exit(0)

# start pump procedure
if __name__ == "__main__":
	try:
		blink_led_test()
	except KeyboardInterrupt:
		GPIO.cleanup
	# force stop the pump after 10 seconds
	# timer = threading.Timer(10, forceClosePump)
	# timer.start

	# if (readHumiditySensor() == 1):
	# 	exitProgram()   	# we don't to washer the flower, it's still humid
	# else:
	# 	while (readHumiditySensor() == 0):
	# 		handleChannelOpen(CHANNEL_1)
	# 		time.sleep(5)

	# 	handleChannelClose(CHANNEL_1)

# release the GPIO
GPIO.cleanup
#!/usr/bin/python

# just for test
print "hello, world!"

# import the necessary modules
import sys
import threading
import time
import timer
import RPi.GPIO as GPIO 

CHANNEL_1 = 26 			# Set GPIO_26 as channel_1 pump

HUMIDITY_SENSOR = 14 	# Set GPIO_21 as humidity sensor

PUMP_OPEN = 1 			# start the pump
PUMP_CLOSE = 0 			# stop the pump

# initialize the GPIO for pump control
GPIO.setmode(GPIO.BCM)
GPIO.cleanup

def gpio_init():
	GPIO.setup(CHANNEL_1, GPIO.OUT)
	GPIO.setup(HUMIDITY_SENSOR, GPIO.IN)

def gpio_deinit():
	GPIO.setup(CHANNEL_1, GPIO.IN)
	GPIO.setup(HUMIDITY_SENSOR, GPIO.IN)

def blink_led_test():
	pins = [26, 19, 13]

	for pin in pins:
		GPIO.setup(pin, GPIO.IN)

	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)

	while True:
		for pin in pins:
			GPIO.output(pin, GPIO.HIGH)
			time.sleep(0.5)
			GPIO.output(pin, GPIO.LOW)
			time.sleep(0.5)

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

def exitProgram():
	# release the GPIO
	forceClosePump()
	gpio_deinit()
	GPIO.cleanup
	sys.exit(0)

def washing(seconds = 10):
	print "I am washing " + seconds + " seconds" 
	handleChannelOpen(CHANNEL_1)
	time.sleep(seconds)
	handleChannelClose(CHANNEL_1)

# start pump procedure
if __name__ == "__main__":
	# try:
	# 	blink_led_test()
	# except KeyboardInterrupt:
	# 	exitProgram()

	gpio_init()

	timer.threading(5, washing(5))

	while True:
		if (readHumiditySensor() == 0):
			continue
		else:
			timer.start
			time.sleep(5)
# release the GPIO
GPIO.cleanup
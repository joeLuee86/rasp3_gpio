#!/usr/bin/python

# just for test
print "hello, world!"

# import the necessary modules
import sys
from threading import Timer
import time
import RPi.GPIO as GPIO 

CHANNEL_1 = 26 			# Set GPIO_26 as channel_1 pump

HUMIDITY_SENSOR = 14 	# Set GPIO_21 as humidity sensor
IS_HUMID = 1 			# Set the humid flag for humidity sensor

PUMP_OPEN = 1 			# start the pump
PUMP_CLOSE = 0 			# stop the pump

PERIOD = 12 * 60 * 60	# washing period

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

def is_dry():
	return readHumiditySensor != IS_HUMID

def forceClosePump():
	handleChannelClose(CHANNEL_1)

def exitProgram():
	# release the GPIO
	forceClosePump()
	gpio_deinit()
	GPIO.cleanup
	sys.exit(0)

def washing(channel = CHANNEL_1, seconds = 10):
	print "I am washing %d seconds"%seconds 
	# we just start the pump only humidity sensor is dry
	if is_dry():
		handleChannelOpen(channel)
		time.sleep(seconds)
		handleChannelClose(channel)


# start pump procedure
if __name__ == "__main__":

	gpio_init()

	if len(sys.argv) < 3:
		# without any valuable info of params
		sys.exit(1)
	else:
		if sys.argv[1] == "channel1":
			if sys.argv[2] == "start":
				washing(CHANNEL_1, 5)
			else:
				handleChannelClose(CHANNEL_1)

	exitProgram()
	
	# test loop
	while True:
		if (readHumiditySensor() == 0):
			continue
		else:
			timer = Timer(PERIOD, washing(5))
			timer.start
			time.sleep(PERIOD)
# release the GPIO
GPIO.cleanup

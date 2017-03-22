#!/usr/bin/python

# just for test
print "hello, world!"

# import the necessary modules
import time
import RPi.GPIO as GPIO 

CHANNEL_1 = 7 		# Set GPIO_7 as channel_1 pump

HUMIDITY_SENSOR = 8 # Set GPIO_8 as humidity sensor

PUMP_OPEN = 1 		# start the pump
PUMP_CLOSE = 0 		# stop the pump

# initialize the GPIO for pump control
GPIO.setmode(GPIO.BOARD)
GPIO.setup(CHANNEL_1, GPIO.OUT)
GPIO.setup(HUMIDITY_SENSOR, GPIO.IN)

# channel handle function
def handleChannelOpen(channel):
	GPIO.output(channel, PUMP_OPEN)

def handleChannelClose(channel):
	GPIO.output(channel, PUMP_CLOSE)

# read humidity sensor info
def readHumiditySensor():
	return GPIO.input(HUMIDITY_SENSOR)

# start pump procedure
if (readHumiditySensor() == 1):
	sys.exit(0)   	# we don't to washer the flower, it's still humid
else:
	while (readHumiditySensor() == 0):
		handleChannelOpen(CHANNEL_1)
		time.sleep(5)
	handleChannelClose(CHANNEL_1)

# release the GPIO
GPIO.cleanup
#!/usr/bin/python
#
# This is GPIO module for simple test and high level abstract API.
# <Joe.luee@outlook.com>
# 2018.10.10
# 
# 					 Raspberry Pi 3B
# 
#                      J8 connector
# 
#                   3V3   	1   2	5V
# 				BCM_2 SDA 	3 	4	5V   
# 				BCM_3 SCL 	5	6	Ground
# 			BCM_4 GPCLK0	7	8	BCM_14 TXD
# 				Ground		9	10	BCM_15 RXD
# 				BCM_17		11	12	BCM_18 PWM0
# 				BCM_27		13	14	Ground
# 				BCM_22		15	16	BCM_23
# 					3V3		17	18	BCM_24
# 			BCM_10 MOSI		19	20	Ground
# 			BCM_9  MISO		21	22	BCM_25
# 			BCM_11 SCLK		23	24	BCM_8 CE0
# 				Ground		25	26	BCM_7 CE1
# 			BCM_0 ID_SD		27 	28 	BCM_1 ID_SC
# 				BCM_5 		29	30 	Ground
# 				BCM_6 		31	32	BCM_12 PWM0
# 			BCM_13 PWM1 	33	34	Ground
# 			BCM_19 MISO 	35 	36 	BCM_16
# 				BCM 26		37	38	BCM_20 MOSI
# 				Ground		39	40	BCM_21 SCLK
# 
# 
# 
# 
#
###################################################################

# import the necessary modules
import sys
from threading import Timer
import time
import copy
import random
import RPi.GPIO as GPIO 

# initialize the GPIO as BCM numbering
GPIO.setmode(GPIO.BCM)

class MyGpio:

	# BCM pins on Raspberry Pi 3B board
	BCM_PINS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

	ONE_MINITE_TICK = 60
	ONE_HOUR_TICK = 60 * ONE_MINITE_TICK 
	HALF_DAY_TICK = 12 * ONE_HOUR_TICK 
	ONE_DAY_TICK = 24 * ONE_HOUR_TICK 
	ONE_MONTH_TICK = 30 * ONE_DAY_TICK

	# initialize all pins as output direction
	def gpio_init_all_output(self):
		for pin in self.BCM_PINS:
			GPIO.setup(pin, GPIO.OUT)

	# initialize all pins as input direction
	def gpio_init_all_input(self):
		for pin in self.BCM_PINS:
			GPIO.setup(pin, GPIO.IN)

	# initialize one pin as output direction
	def gpio_init_output(self, pin_number):
		GPIO.setup(pin_number, GPIO.OUT)

	# initialize one pin as output direction
	def gpio_init_input(self, pin_number):
		GPIO.setup(pin_number, GPIO.IN)	

	# clear all pins
	def gpio_all_clear(self):
		for pin in self.BCM_PINS:
			GPIO.output(pin, GPIO.LOW) 

	# set all pins
	def gpio_all_set(self):
		for pin in self.BCM_PINS:
			GPIO.output(pin, GPIO.HIGH)

	# set one pin
	def gpio_set(self, pin):
		GPIO.output(pin, GPIO.HIGH)

	# clear one pin
	def gpio_clear(self, pin):
		GPIO.output(pin, GPIO.LOW)

	####################################################
	#  LED related function
	def gpio_led_lights_on(self, number, tick):
		for pin in range(0, number):
			print pin
			GPIO.output(pin, GPIO.HIGH)
			time.sleep(tick)
			GPIO.output(pin, GPIO.LOW)
			time.sleep(tick)


	####################################################
	
	# LED Toggle show, GPIO high for light on, low for light off
	# It will just toggle all LED one by one, and reverse once
	def gpio_led_toggle_show_once(self, tick = 1):
		# init all pins as ouput for LED toggle show
		self.gpio_init_all_output()

		# clear all LED before show
		self.gpio_all_clear()

		for pin in self.BCM_PINS:
			print pin
			GPIO.output(pin, GPIO.HIGH)
			time.sleep(tick)
			GPIO.output(pin, GPIO.LOW)
			time.sleep(tick)

		BCM_REVERSE_PINS = copy.copy(self.BCM_PINS)
		BCM_REVERSE_PINS.reverse()
		for pin in BCM_REVERSE_PINS:
			print pin
			GPIO.output(pin, GPIO.HIGH)
			time.sleep(tick)
			GPIO.output(pin, GPIO.LOW)
			time.sleep(tick)	

		# clear all LED before quit
		self.gpio_all_clear()

	# LED toggle dragon
	def gpio_led_toggle_dragon(self):
		while True:
			self.gpio_led_toggle_show_once(0.5)

	# LED balancer
	def gpio_led_balancer_random(self):

		while True:
			leds = int(random.random() * len(self.BCM_PINS))
			self.gpio_led_lights_on(leds, 0.3)



# start LED test
if __name__ == "__main__":

	# create object
	mygpio = MyGpio()

	mygpio.gpio_init_all_output()

	mygpio.gpio_led_toggle_show_once(0.5)

	# time.sleep(2)

	# for i in range(1, 10):
	# 	mygpio.gpio_led_toggle_show_once(0.3)

	# time.sleep(2)
	
	# mygpio.gpio_led_balancer_random()



# release the GPIO
GPIO.cleanup
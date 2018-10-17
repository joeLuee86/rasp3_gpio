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
import string
import RPi.GPIO as GPIO 

# initialize the GPIO as BCM numbering
GPIO.setmode(GPIO.BCM)

class MyGpio:

	# BCM pins on Raspberry Pi 3B board
	# BCM_PINS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
	BCM_PINS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

	BAMP = 27

	BCM_BUTTONS = {'LEFT' : 21, 'MIDDLE' : 26, 'RIGHT' : 20}

	ONE_MINITE_TICK = 60
	ONE_HOUR_TICK = 60 * ONE_MINITE_TICK 
	HALF_DAY_TICK = 12 * ONE_HOUR_TICK 
	ONE_DAY_TICK = 24 * ONE_HOUR_TICK 
	ONE_MONTH_TICK = 30 * ONE_DAY_TICK

	# initialize all pins as output direction
	def gpio_init_all_output(self):
		GPIO.setup(self.BAMP, GPIO.OUT)
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
			self.gpio_led_toggle_show_once(0.1)

	# LED balancer
	def gpio_led_balancer_random(self, times):

		for i in range(1, times):
			leds = int(random.random() * len(self.BCM_PINS)) + 1
			self.gpio_led_lights_on(leds, 0.05)
			time.sleep(0.2)

	# LED boxer
	def gpio_led_boxer(self, times):
		ORG_PINS = self.BCM_PINS
		BCM_REVERSE_PINS = copy.copy(ORG_PINS)
		BCM_REVERSE_PINS.reverse()

		COMB_PINS_INCREASE = ORG_PINS + BCM_REVERSE_PINS
		COMB_PINS_DECREASE = BCM_REVERSE_PINS + ORG_PINS

		for i in range(1, times):
			for pin in range(0, len(ORG_PINS)):
				GPIO.output(COMB_PINS_INCREASE[pin], GPIO.HIGH)
				GPIO.output(COMB_PINS_DECREASE[pin], GPIO.HIGH)
				time.sleep(0.05)
				GPIO.output(COMB_PINS_INCREASE[pin], GPIO.LOW)
				GPIO.output(COMB_PINS_DECREASE[pin], GPIO.LOW)
				time.sleep(0.05)
				print COMB_PINS_INCREASE[pin]
				print COMB_PINS_DECREASE[pin]
		

	#############################################################
	# Buttons

	# initiate buttons pin, low is pressed.
	def gpio_buttons_init(self):
		for (button, pin) in self.BCM_BUTTONS.items():
			GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def gpio_buttons_detect(self):

		for (button, pin) in self.BCM_BUTTONS.items():
			if (GPIO.input(pin) == 0):
				time.sleep(0.01)
				if (GPIO.input(pin) == 0):
					time.sleep(0.01)
					return button
		return "NULL"

	def print_n_stars(self, offset, number):
		if number > len(self.BCM_PINS):
			return

		star_str = ''
		if (offset == 0):
			for i in range(0, number):
				star_str += '*'
		else:
			for i in range(0, offset):
				star_str += ' '

			for i in range(0, number):
				star_str += '*'

		print star_str

		for i in range(0, len(star_str)):
			if star_str[i] == '*':
				GPIO.output(self.BCM_PINS[i], GPIO.HIGH)

# start LED test
if __name__ == "__main__":

	# create object
	mygpio = MyGpio()

	mygpio.gpio_init_all_output()

	mygpio.gpio_buttons_init()

	mygpio.gpio_led_toggle_show_once(0.2)

	time.sleep(2)

	num_stars = sys.argv[1]
	print "You want to print " + num_stars + " stars tower!"

	n_stars = int(num_stars)
	for i in range(0, n_stars):
		mygpio.print_n_stars((n_stars - i - 1), (2 * i + 1))
		time.sleep(1)
		mygpio.gpio_all_clear()

	# while True:

	# 	button = mygpio.gpio_buttons_detect() 
	# 	if button != "NULL":
	# 		print button

	# 	if button == "RIGHT":
	# 		GPIO.output(mygpio.BAMP, GPIO.HIGH)

	# 	if button == "MIDDLE":
	# 		GPIO.output(mygpio.BAMP, GPIO.LOW)

	# 	time.sleep(0.3)

		# for i in range(1, 8):
		# 	mygpio.gpio_led_toggle_show_once(0.05)

		# time.sleep(2)

		# mygpio.gpio_led_balancer_random(20)

		# time.sleep(2)
		
		# mygpio.gpio_led_boxer(20)

		# time.sleep(2)



# release the GPIO
GPIO.cleanup

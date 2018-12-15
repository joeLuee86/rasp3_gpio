#!/usr/bin/python
#
# Simple Motor Control module for ST L298N H-bridge DC driver.
# <Joe.luee@outlook.com>
# 2018.12.10
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
import re,sys
from threading import Timer
import time
import copy
import random
import string
import threading
import thread
import socket

import RPi.GPIO as GPIO 

# initialize the GPIO as BCM numbering
GPIO.setmode(GPIO.BCM)


class MotorControl:

	OUT_PUT_A = 0

	OUT_PUT_B = 1

	OUT_PUT_PWMS = 4

	motorDutyCycle = 0

	direction_val = 0  # 0 - clock-wise; 1 - anti-clock wise.

	def pin_init(self, outA, outB, pwm):

		self.OUT_PUT_A = outA
		self.OUT_PUT_B = outB
		self.OUT_PUT_PWMS = pwm

		GPIO.setup(self.OUT_PUT_A, GPIO.OUT)
		GPIO.setup(self.OUT_PUT_B, GPIO.OUT)
		GPIO.setup(self.OUT_PUT_PWMS, GPIO.OUT)


	def forward(self):
		if self.direction_val:
			self.move_forward()
		else:
			self.move_back()


	def reverse(self):
		if self.direction_val:
			self.move_back()
		else:
			self.move_forward()


	def brake(self):
		GPIO.output(self.OUT_PUT_A, GPIO.LOW)
		GPIO.output(self.OUT_PUT_B, GPIO.LOW)


	def toggle_direction(self):
		self.direction_val = ~self.direction_val


	def move_back(self):
		GPIO.output(self.OUT_PUT_A, GPIO.HIGH)
		GPIO.output(self.OUT_PUT_B, GPIO.LOW)


	def move_forward(self):
		GPIO.output(self.OUT_PUT_A, GPIO.LOW)
		GPIO.output(self.OUT_PUT_B, GPIO.HIGH)


	def speed(self, val):
		self.motorDutyCycle.ChangeDutyCycle(val)		# range 0 - 100
	

	def start(self, freq):
		self.motorDutyCycle = GPIO.PWM(self.OUT_PUT_PWMS, freq)
		self.motorDutyCycle.start(0)


	def stop(self):
		self.motorDutyCycle.stop()




class SuperTank:
	motor_1 = MotorControl()
	motor_1.pin_init(7, 8, 1)

	motor_2 = MotorControl()
	motor_2.pin_init(9, 10, 0)


	# init HC-SR04 ultrsonic distance detector
	FRONT_TRIG = 15
	FRONT_ECHO = 14

	BACK_TRIG  = 3
	BACK_ECHO  = 2

	GPIO.setup(FRONT_TRIG, GPIO.OUT)	# Front Trig 
	GPIO.setup(FRONT_ECHO, GPIO.IN)		# Front Echo

	GPIO.setup(BACK_TRIG, GPIO.OUT)	# Back Trig 
	GPIO.setup(BACK_ECHO, GPIO.IN)		# Back Echo

	BARRIER_TOLERANCE = 30    # the minim distance to barrier, cm

	def barrier_front(self):
		GPIO.output(self.FRONT_TRIG, GPIO.LOW)
		time.sleep(0.05)
		# trig pulse
		GPIO.output(self.FRONT_TRIG, GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(self.FRONT_TRIG, GPIO.LOW)

		while GPIO.input(self.FRONT_ECHO) == 0 :
			start = time.time()

		while GPIO.input(self.FRONT_ECHO) == 1 :
			stop = time.time()

		return int((stop - start) * 340 * 100 / 2)   # distance with cm unit

	def barrier_back(self):
		GPIO.output(self.BACK_TRIG, GPIO.LOW)
		time.sleep(0.05)
		# trig pulse
		GPIO.output(self.BACK_TRIG, GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(self.BACK_TRIG, GPIO.LOW)

		while GPIO.input(self.BACK_ECHO) == 0 :
			start = time.time()

		while GPIO.input(self.BACK_ECHO) == 1 :
			stop = time.time()

		return int((stop - start) * 340 * 100 / 2)  # distance with cm unit

	def start(self, freq):
		self.motor_1.start(freq)
		self.motor_2.start(freq)

	def stop(self):
		self.motor_1.stop()
		self.motor_2.stop()

	def go_forward(self):
		self.motor_1.forward()
		self.motor_2.forward()

		return 0

	def go_back(self):
		self.motor_1.reverse()
		self.motor_2.reverse()

		return 0

	def turn_right(self, dir):
		if dir == 1:
			self.motor_1.brake()
			self.motor_2.forward()
		else:
			self.motor_1.brake()
			self.motor_2.reverse()

	def turn_left(self, fir):
		if dir == 1:
			self.motor_2.brake()
			self.motor_1.forward()
		else:
			self.motor_2.brake()
			self.motor_1.reverse()
			

	def rotate_clock(self):
		self.motor_1.forward()
		self.motor_2.reverse()

	def rotate_anti_clock(self):
		self.motor_1.reverse()
		self.motor_2.forward()

	def accelerate(self, val):
		self.motor_1.speed(val)
		self.motor_2.speed(val)

	def brake(self):
		self.motor_1.brake()
		self.motor_2.brake()

	def adjust_barrier_tolerance(self, tolerance):
		if tolerance > 2:
			self.BARRIER_TOLERANCE = tolerance



# def is_number(s):
#     try:
#         float(s)
#         return True
#     except ValueError:
#         pass
 
#     try:
#         import unicodedata
#         unicodedata.numeric(s)
#         return True
#     except (TypeError, ValueError):
#         pass
 
#     return False


# Global variables

is_front_barrier = 1
is_back_barrier = 1


SLOPE = 0.05

PARSE_LOCK = 0


def parse_command(tank, command):
	print command
	PARSE_LOCK = 1
	if len(command) < 6:
		return

	angle = int(command[1])
	strength = int(command[3])

	if angle < 120 and angle > 60:
		# should forward
		if is_front_barrier == 0:
			tank.go_forward()
			tank.accelerate(strength)
		else:
			tank.brake()

	elif angle <= 60:
		# turn forward right
		print "turn forward right"
		tank.turn_right(1)
		tank.accelerate(strength)

	elif angle >= 300:
		# turn back left
		print "turn back right"
		tank.turn_right(0)
		tank.accelerate(strength)

	elif angle >= 120 and angle <= 180:
		# turn right
		print "turn forward left"
		tank.turn_left(1)
		tank.accelerate(strength)

	elif angle > 180 and angle <= 240:
		print "turn back left"
		tank.turn_left(0)
		tank.accelerate(strength)

	elif angle > 240 and angle < 300:
		# go left
		if is_back_barrier == 0:
			tank.go_back()
			tank.accelerate(strength)
		else:
			tank.brake()

	PARSE_LOCK = 0

def my_tank_task(name, val):

	myTank = SuperTank()

	myTank.brake() 

	myTank.start(100)   # PWM with 100HZ

	mySocket = socket.socket()
	host = socket.gethostname()
	port = 1234
	mySocket.bind(("192.168.1.106", port))

	mySocket.listen(5)

	client, address = mySocket.accept()
	print "A client connected: IP:", address 

	while True:
		if PARSE_LOCK == 0:

			c, addr = mySocket.accept()     # ????????

			RECV_BUF = " "

			RECV_BUF = c.recv(1024)

			# report format: 
			# Command:parameter
			# E.X
			# 		angle:90:strength:50:tolerance:5
			# 		angle:45:strength:90:tolerance:5
			myList = RECV_BUF.split(":")
			parse_command(myTank, myList)



		

if __name__ == "__main__":
	myTank = SuperTank()

	thread.start_new_thread(my_tank_task, ("tank_task", 1))

	while(1):
		time.sleep(0.1)

		if myTank.barrier_front() < myTank.BARRIER_TOLERANCE:
			is_front_barrier = 1
		else:
			is_front_barrier = 0

		if myTank.barrier_back() < myTank.BARRIER_TOLERANCE:
			is_back_barrier = 1
		else:
			is_back_barrier = 0



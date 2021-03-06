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
import os
from threading import Timer
import time
import copy
import random
import string
import threading
import thread
import socket
import math

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
		if (val > 100 or val < 0):
			return
		self.motorDutyCycle.ChangeDutyCycle(val)		# range 0 - 100
	

	def start(self, freq):
		self.motorDutyCycle = GPIO.PWM(self.OUT_PUT_PWMS, freq)
		self.motorDutyCycle.start(0)


	def stop(self):
		self.motorDutyCycle.stop()




class SuperTank:
	motor_1 = MotorControl()
	#motor_1.pin_init(7, 8, 1)
	motor_1.pin_init(9, 10, 0)
	
	motor_2 = MotorControl()
	#motor_2.pin_init(9, 10, 0)
	motor_2.pin_init(7, 8, 1)


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

	def go_forward(self, acc_left, acc_right):
		self.motor_1.forward()
		self.motor_2.forward()
		self.motor_1.speed(acc_left)
		self.motor_2.speed(acc_right)	

		return 0

	def go_back(self, acc_left, acc_right):
		self.motor_1.reverse()
		self.motor_2.reverse()
		self.motor_1.speed(acc_left)
		self.motor_2.speed(acc_right)	

		return 0

	def turn_right(self, acc):
		self.motor_2.brake()
		self.motor_1.forward()

		self.motor_1.speed(acc)
		self.motor_2.speed(acc)	

	def turn_left(self, acc):
		self.motor_1.brake()
		self.motor_2.forward()

		self.motor_1.speed(acc)
		self.motor_2.speed(acc)	
			

	def rotate_clock(self, acc):
		self.motor_1.forward()
		self.motor_2.reverse()
		self.motor_1.speed(acc)
		self.motor_2.speed(acc)	

	def rotate_anti_clock(self, acc):
		self.motor_1.reverse()
		self.motor_2.forward()
		self.motor_1.speed(acc)
		self.motor_2.speed(acc)	

	def accelerate(self, val):
		self.motor_1.speed(val)
		self.motor_2.speed(val)

	def brake(self):
		self.motor_1.brake()
		self.motor_2.brake()
		# self.motor_1.speed(0)
		# self.motor_2.speed(0)	

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
	# print command
	PARSE_LOCK = 1
	if len(command) < 6:
		return

#	tank.go_forward(40, 40)
#	time.sleep(0.1)
	tank.brake()
	angle = int(command[1])
	strength = int(command[3])

	# if angle < 100 and angle > 80:
	# 	# should straight forward
	# 	if is_front_barrier == 0:
	# 		tank.go_forward(strength, strength)
	# 	else:
	# 		tank.brake()

	if angle <= 90 and angle >= 20:
		# turn forward right
		# print "turn forward right"
		if is_front_barrier == 0:
			acc_right = int(abs(math.sin(angle * math.pi / 180) * strength))
			# print "strength = ", strength, " acc_right = ", acc_right
			tank.go_forward(strength, acc_right)
		else:
			tank.brake()		

	elif angle > 90 and angle <= 160:
		# turn forward left
		# print "turn forward left"
		if is_front_barrier == 0:
			acc_left = int(abs(math.sin(angle * math.pi / 180) * strength))
			# print "acc_left = ", acc_left, " strength = ", strength
			tank.go_forward(acc_left, strength)
		else:
			tank.brake()

	elif angle >= 270 and angle <= 340:
		# turn back right
		# print "turn back right"
		if is_back_barrier == 0:
			acc_right = int(abs(math.sin(angle * math.pi / 180) * strength))
			# print "strength = ", strength, " acc_right = ", acc_right
			tank.go_back(strength, acc_right)
		else:
			tank.brake()

	elif angle < 20 or angle > 340:
	 	# turn right
	 	tank.turn_right(strength)

	elif angle > 160 and angle < 200:
	 	# turn left
	 	tank.turn_left(strength)

	elif angle >= 200 and angle < 270:
		# print "turn back left"
		if is_back_barrier == 0:
			acc_left = int(abs(math.sin(angle * math.pi / 180) * strength))
			# print "acc_left = ", acc_left, " strength = ", strength
			tank.go_back(acc_left, strength)
		else:
			tank.brake()

	# elif angle > 260 and angle < 280:
	# 	# go left
	# 	if is_back_barrier == 0:
	# 		tank.go_back(strength, strength)
	# 	else:
	# 		tank.brake()

	PARSE_LOCK = 0



def my_tank_task(name, val):

	myTank = SuperTank()

	myTank.brake() 

	myTank.start(100)   # PWM with 100HZ

#	myTank.go_forward(35, 35)

#	time.sleep(1)

#	myTank.brake()

	try:
		mySocket = socket.socket()
		host = socket.gethostname()
		port = 1234
		mySocket.bind(("192.168.43.93", port))
	except Exception:
		print "socket binding error"
		mySocket.close()
		return -1

	mySocket.listen(5)

	client, address = mySocket.accept()
	print "A client connected: IP:", address 

	recv = " "
	RECV_BUF = " "
	while True:
		if PARSE_LOCK == 0:

			c, addr = mySocket.accept()     # ????????
#			print "connected client: ", addr
#			RECV_BUF = " "

			temp_buf = c.recv(1024)
			if len(temp_buf) < 30:
				RECV_BUF += temp_buf
				temp_buf = c.recv(1024)
				RECV_BUF += temp_buf
				# print RECV_BUF
				myList = RECV_BUF.split(":")
				parse_command(myTank, myList)
				RECV_BUF = " "

#			buf = client.recv(1024)
#			if not len(buf):
#				recv += buf
#				break
#			else:
#				recv += buf
#				print recv
#				recv = " "
#			print buf

			# report format: 
			# Command:parameter
			# E.X
			# 		angle:90:strength:50:tolerance:5
			# 		angle:45:strength:90:tolerance:5
#			myList = RECV_BUF.split(":")
#			parse_command(myTank, myList)

	mySocket.close()
	return 0

def is_front_barrier(tank):
	if tank.barrier_front() < tank.BARRIER_TOLERANCE:
		return 1
	else:
		return 0

def is_back_barrier(tank):
	if tank.barrier_back() < tank.BARRIER_TOLERANCE:
		return 1
	else:
		return 0

def free_walk():

	my_tank = SuperTank()

	my_tank.brake() 

	my_tank.start(100)

	for i in range(0, 100):
		print "we are in for loop %d" %(i)
		time.sleep(0.3)
		if is_front_barrier(my_tank):
			print "front barrier 1"
			my_tank.go_back(40, 40)
			time.sleep(0.3)
			my_tank.go_forward(0, 40)
			time.sleep(0.3)     # turn right
			my_tank.brake()
			if is_front_barrier(my_tank):
				print "front barrier 2"
				my_tank.go_forward(0, 40)
				time.sleep(0.3)
				if is_front_barrier(my_tank):
					print "front barrier 3"
					my_tank.go_back(40, 40)
					time.sleep(0.2)
					my_tank.go_forward(40, 0)
					time.sleep(0.6)
					my_tank.brake()
		elif is_back_barrier(my_tank):
			print "back barrier 1"
			my_tank.go_forward(40, 40)
			time.sleep(0.3)
			my_tank.brake()

		else:
			my_tank.go_forward(40, 40)








if __name__ == "__main__":
	myTank = SuperTank()

	myTank.brake() 

	myTank.start(100)

	#free_walk()

	#sys.exit(0)

#	myTank.go_forward(50 , 50)

#	time.sleep(1)

#	myTank.brake()

	try :
		thread.start_new_thread(my_tank_task, ("tank_task", 1))

		while(1):
			time.sleep(0.02)
	#		is_front_barrier = 0
	#		is_back_barrier  = 0
	
			if myTank.barrier_front() < myTank.BARRIER_TOLERANCE:
				is_front_barrier = 1
			else:
				is_front_barrier = 0

			if myTank.barrier_back() < myTank.BARRIER_TOLERANCE:
				is_back_barrier = 1
			else:
				is_back_barrier = 0

			# print "is_front_barrier = ", is_front_barrier, " is_back_barrier = ", is_back_barrier

	except Exception:
		print "socket task break"
		os.system("sudo service my_tank restart")

	os.system("sudo service my_tank restart")	


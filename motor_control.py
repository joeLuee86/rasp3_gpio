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
import sys
from threading import Timer
import time
import copy
import random
import string
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


	def move_forward(self):
		GPIO.output(self.OUT_PUT_A, GPIO.HIGH)
		GPIO.output(self.OUT_PUT_B, GPIO.LOW)


	def move_back(self):
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

	def start(self, freq):
		self.motor_1.start(freq)
		self.motor_2.start(freq)

	def stop(self):
		self.motor_1.stop()
		self.motor_2.stop()

	def go_forward(self):
		self.motor_1.forward()
		self.motor_2.forward()

	def go_back(self):
		self.motor_1.reverse()
		self.motor_2.reverse()

	def turn_left(self):
		self.motor_1.brake()
		self.motor_2.forward()

	def turn_right(self):
		self.motor_1.forward()
		self.motor_2.brake()

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


if __name__ == "__main__":


	tank = SuperTank()

	tank.brake()

	tank.start(100)    # PWM with 100 HZ frequency

	for i in range(1, 100):
		time.sleep(0.1)
		tank.go_forward()
		tank.accelerate(i)

	for i in range(1, 100):
		time.sleep(0.1)
		tank.go_back()
		tank.accelerate(i)

	for i in range(1, 100):
		time.sleep(0.1)
		tank.rotate_clock()
		tank.accelerate(i)

	for i in range(1, 100):
		time.sleep(0.1)
		tank.rotate_anti_clock()
		tank.accelerate(i)

	tank.brake()

	tank.stop()






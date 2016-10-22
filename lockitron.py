# Darin Chin
# Lockitron class
# 7/04/2016
'''
make sure you have the RPi.GPIO library

IMPORTANT: 	follow this pin-out mapping https://pinout.xyz/ for raspberry pi (FOLLOW THE BCM NUMBERS)
			use this driver -- https://www.sparkfun.com/products/9457
			make sure external battery is atleast 9V with atleast 550 mA
Connect the pins as follow:
	Switches on lock = BCM number on raspberry pi pinout:
	1A = 0
	2A = 5
	1B = 6
	2B = 13
	ALL SWITCH GROUNDS = GROUND

	Lock Motor = pin on driver:
	(+) = A01
	(-) = A02

	pin on driver = BCM number on raspberry pi:
	PWMA = 12
	AIN1 = 24
	AIN2 = 23
	STBY = 3.3V rpi
	VCC = 3.3V rpi

	VM = 9V external battery on breadboard 
	ALL GND PINS = Ground on the breadboard
'''
import RPi.GPIO as GPIO
import time

class Lockitron():
	# Constants
	LOCK_OPEN = 0
	LOCK_CLOSED = 1

	# Motor speed/directions
	MOTOR_SPEED = 70
	MOTOR_CW = 0
	MOTOR_CCW = 1

	# Pin Mapping
	# USE THIS WEBSITE TO FIND ON-BOARD MAPPING https://pinout.xyz/
	# USE BCM PIN numbers 
	# UNLOCK_PIN = 27
	# LOCK_PIN = 22 # Probably don't need these pins, if needed make sure to uncomment line 35
	SW_1A_PIN = 0
	SW_1B_PIN = 6
	SW_2A_PIN = 5
	SW_2B_PIN = 13
	AIN1_PIN = 24
	AIN2_PIN = 23
	PWMA_PIN = 12

	# Outputs/Inputs/Input pullup
	OUTPUTS = [AIN1_PIN, AIN2_PIN, PWMA_PIN]
	INPUT_PULLUPS = [SW_1A_PIN, SW_1B_PIN, SW_2A_PIN, SW_2B_PIN]
	# INPUTS = [UNLOCK_PIN, LOCK_PIN] #probably don't need this either

	# Button states (boolean values)
	btn_lock = None
	btn_unlock = None
	prev_btn_lock = 1 
	prev_btn_unlock = 1

	# Switch states
	sw_1a = None
	sw_1b = None
	sw_2a = None
	sw_2b = None

	# Lock state
	lock_state = None

	# PWMA pin
	pwma_pin = None

	def __init__(self):
		# set pins to outputs/inputs
		GPIO.setmode(GPIO.BCM)

		GPIO.setup(OUTPUTS, GPIO.OUT)
		GPIO.setup(INPUTS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(INPUT_PULLUPS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		global pwma_pin
		pwma_pin = GPIO.PWM(PWMA_PIN, MOTOR_SPEED)

	# no longer needed
	# def lock():
	# # move motor to lock bolt
	# print ("locking...")
	# move_motor(MOTOR_SPEED, MOTOR_CW)

	# # read 
	# global sw_1a, sw_1b, sw_2a, sw_2b, lock_state
	# while True:
	# 	sw_1a = GPIO.input(SW_1A_PIN)
	# 	sw_1b = GPIO.input(SW_1B_PIN)
	# 	sw_2a = GPIO.input(SW_2A_PIN)
	# 	sw_2b = GPIO.input(SW_2B_PIN)


	# 	if ((sw_1a == 0) and (sw_1b == 1) and (sw_2a == 0) and (sw_2b == 1)):
	# 		break

	# stop_motor()
	# time.sleep(0.1)

	# # move motor to home position
	# move_motor(MOTOR_SPEED, MOTOR_CCW)

	# while True:
	# 	sw_1a = GPIO.input(SW_1A_PIN)
	# 	sw_1b = GPIO.input(SW_1B_PIN)
	# 	sw_2a = GPIO.input(SW_2A_PIN)
	# 	sw_2b = GPIO.input(SW_2B_PIN)
	# 	if ((sw_2a == 1) and (sw_2b == 1)):
	# 		break

	# stop_motor()
	# print("done locking.")
	# lock_state = LOCK_OPEN

	def unlock():
		# move motor to unlock bolt
		print ("unlocking...")
		move_motor(MOTOR_SPEED, MOTOR_CCW)
		global sw_1a, sw_1b, sw_2a, sw_2b, lock_state
		# read 
		while True:
			sw_1a = GPIO.input(SW_1A_PIN)
			sw_1b = GPIO.input(SW_1B_PIN)
			sw_2a = GPIO.input(SW_2A_PIN)
			sw_2b = GPIO.input(SW_2B_PIN)
			
			if ((sw_2b == 1) and (sw_1b == 1)):
				break
		stop_motor()
		time.sleep(0.1)

	def lock():
		# move motor to reset position
		print ("reseting lock")
		move_motor(MOTOR_SPEED, MOTOR_CCW)
		global sw_1a, sw_1b, sw_2a, sw_2b

		while True:

			sw_1a = GPIO.input(SW_1A_PIN)
			sw_1b = GPIO.input(SW_1B_PIN)
			sw_2a = GPIO.input(SW_2A_PIN)
			sw_2b = GPIO.input(SW_2B_PIN)
		
			
			if ((sw_2a == 1) and (sw_1a == 1)):
				break
		stop_motor()

	def move_motor(speed, direction):
		# ain1 is CCW, ain2 is CW

		ain1 = 0
		ain2 = 0

		if (direction):
			ain1 = 1
			ain2 = 0
		else:
			ain1 = 0
			ain2 = 1

		# set AIN1_PIN to ain1
		GPIO.output(AIN1_PIN, ain1)
		GPIO.output(AIN2_PIN, ain2)
		# set AIN2_PIN to ain2
		# set pwma_pin to speed
		global pwma_pin
		pwma_pin.start(speed)
		print ("starting motor")

	def stop_motor():
		# set PWMA_PIN to 0
		print ("stopping motor")
		global pwma_pin
		pwma_pin.stop()

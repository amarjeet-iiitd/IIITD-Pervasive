import RPi.GPIO as GPIO
import time

def PIR_Read():
	GPIO_pin = 18

	GPIO.setmode(GPIO.BCM)

	GPIO.setup(GPIO_pin, GPIO.IN)

	return GPIO.input(GPIO_pin)
	
'''
while True:
	print('PIR Value : ', PIR_Read())
	time.sleep(1)
'''


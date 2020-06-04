import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)

COUNT_DATA=5000

while(COUNT_DATA):
	status = GPIO.input(18)
	print(status)
	time.sleep(0.000025)		
	COUNT_DATA-=1
	
GPIO.cleanup() 

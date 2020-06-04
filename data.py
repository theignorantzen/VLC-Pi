import RPi.GPIO as GPIO
import binascii
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
	
st="110101010100100001101111011011000110000100000000"

while True:
	for j in st:
		if j=='1':
			GPIO.output(23, GPIO.HIGH)
			time.sleep(0.0025)		
		else:
			GPIO.output(23, GPIO.LOW)
			time.sleep(0.0025)

GPIO.cleanup()

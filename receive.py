import RPi.GPIO as GPIO
import binascii
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)

COUNT_DATA=5000
a = [1, 1, 0, 1, 0, 1, 0, 1]
x = [0, 0, 0, 0, 0, 0, 0, 0]

f = open('output.txt','a')

while(COUNT_DATA):
	status = GPIO.input(18)
	time.sleep(0.000025)	
	x.pop(0)
	x.append(status)
	count = 0
	for i in range(8):
		if x[i] == a[i]:
			count += 1
	if count == 8:
		f.write('x')
		for j in range(32):
			data = GPIO.input(18)
			time.sleep(0.000025)
			f.write(data)

	COUNT_DATA-=1

f.close()	
GPIO.cleanup() 
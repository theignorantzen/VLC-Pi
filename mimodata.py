import RPi.GPIO as GPIO
import binascii
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

pin = [12, 16, 5, 6, 13, 19]
k = 0

st="110101011010111"

cols = 6
rows = len(st)/3
arr = [[0]*cols]*rows

for i in range(rows):
	if st[k] == '0':
		arr[i][0] = 1
	else:
		arr[i][1] = 1
	if st[k+1] == '0' and st[k+2] == '0':
		arr[i][2] = 1
	elif st[k+1] == '0' and st[k+2] == '1':
		arr[i][3] = 1
	elif st[k+1] == '1' and st[k+2] == '0':
		arr[i][4] = 1
	elif st[k+1] == '1' and st[k+2] == '1':
		arr[i][5] = 1
	k = k+3

while True:
	for i in range(rows):
		for j in range(cols):
			GPIO.output(pin[j], arr[i][j])
		time.sleep(0.01)

GPIO.cleanup()
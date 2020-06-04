import RPi.GPIO as GPIO
import binascii
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(7, GPIO.IN)
GPIO.setup(11, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(15, GPIO.IN)

pin = [23, 24, 7, 11, 13, 15]

count = 1000
arr = [0]*count

while count:
	for i in range(6):
		arr[1000-count] = GPIO.input(pin[i])
	time.sleep(0.01)
	count -= 1

for i in range(1000):
	print(a[i], end =" ")

'''arr = [0]*n
for i in n:
	arr[i] = GPIO.input(pin[i])
if arr[0] == 1:
	print("1")
else:
	print("0")
if arr[2] == 1:
	print("00")
elif arr[3] == 1:
	print("01")
elif arr[4] == 1:
	print("10")
elif arr[5] == 1:
	print("11") '''

GPIO.cleanup()
	
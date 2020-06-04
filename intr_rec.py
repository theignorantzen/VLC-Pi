from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#list of all pins
pin = [23, 24, 7, 11, 13, 15]
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(pin, GPIO.BOTH, callback=status, bouncetime=2)
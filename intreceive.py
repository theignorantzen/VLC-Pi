from Adafruit_CharLCD import Adafruit_CharLCD

lcd = Adafruit_CharLCD(rs=22, en=23, d4=24, d5=25, d6=26, d7=27, cols=16, lines=2)
lcd.clear()
lcd.blink(True)            # turn on blinking cursor

row = 0                    # variable to hold row position
col = 0                    # variable to hold column position
line = ''                  # variable to hold line display

from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering

# Set up all input pins (pass tuple of GPIO pins)
channel_list =[20,21,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
GPIO.setup(channel_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set initial display line
if GPIO.input(16):
    row = 0    # First Line
else:
    row = 1    # Second Line
lcd.setCursor(col, row)

# Callback function to run in another thread when toggle switch state changes
def toggleChanged(channel):
    global col, row, line
    col = 0
    if GPIO.input(16):     # True = Rising = First Line (decimal)
        print "Toggle to Decimal row"
        row = 0
        if not line:
            lcd.clear()
        else:
            lcd.setCursor(col, row)
            lcd.message('{0:d}'.format(int(line, 16)))
    else:                  # False = Falling = Second Line (hex)
        print "Toggle to Hex row"
        row = 1
        if not line:
            lcd.clear()
            lcd.setCursor(col, row)
        else:
            lcd.setCursor(col, row)
            lcd.message('{0:x}'.format(int(line)))
    line = ''
    
# Callback function to run in another thread when keypad pressed
def keypadPressed(channel):
    if channel == 20 or channel == 21:
        channel -= 20      # Adjust for keys 0 & 1 on GPIO 20 & 21
    
    global col, row, line
    if row == 0 and channel > 9:
        pass               # First line is for decimal (no hex) 
    elif col < 16:
        key = '{0:x}'.format(channel)  # Format key to hex string
        line += key
        print 'Keypad pressed: ' + key
        lcd.setCursor(col, row)
        lcd.message(key)
        col += 1
    else:
        print 'Line full: ' + line
        dec = int(line, 16)
        
# listen for changing edge on toggle switch (both directions)
# event will interrupt the program and call the toggleLine function
GPIO.add_event_detect(16, GPIO.BOTH, callback=toggleChanged, bouncetime=300)

# exclude toggle pin
channel_list.pop();
# loop through channels and add event for each button on keypad
for pin in channel_list:
    GPIO.add_event_detect(pin, GPIO.RISING, callback=keypadPressed, bouncetime=150) 

try:
    while True:
        sleep(1)         # wait 1 second

finally:                   # run on exit
    GPIO.cleanup()         # clean up
    print "All cleaned up."
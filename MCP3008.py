import spidev
import time
import os

#Open SPI bus
spi = spidev.SpiDev()
spi.open (0,0)
spi.max_speed_hz=1000000

#Function to read SPI data from MCP3008 chip
#Channel must be an int 0-7
def ReadChanel(channel):
	adc = spi.xref2([1,(8+channel)<<4,0])
	data = ((adc[1]&3)<<8) + adc[2]
	return data

#Functio to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts


while True:

  # Read the light sensor data
  light_level = ReadChannel(1)
  light_volts = ConvertVolts(light_level,2)

  # Print out results
  print "--------------------------------------------"
  print("Light: {} ({}V)".format(light_level,light_volts))

  # Wait before repeating loop
  time.sleep(1)
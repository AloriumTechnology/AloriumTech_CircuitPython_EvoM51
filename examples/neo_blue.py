"""
`neo_blue`
========================================================
Copyright 2020 Alorium Technology

Contact: info@aloriumtech.com

Description:

This is a very simple CircuitPython program that turns the
Evo M51 NeoPixel blue.

It also shows an example of how the FPGA I/O is configured 
via the I2C interface between the devices.  As referenced 
below, the explicit I2C calls will not be required once 
an Evo M51 board libary is complete.

"""

import board
import neopixel
import digitalio

import alorium_evom51 as evo

# Enable the FPGA pin that controls D8 (NeoPixel) and set as an output
# These explicit I2C calls will not be required once an Evo M51 board libary is complete 
evo.i2c1.writeto(0x08, bytes([0x20, evo.D2F_ENSET_ADDR, 0x00, 0x20, 0x00, 0x00]), stop=False)
evo.i2c1.writeto(0x08, bytes([0x20, evo.D2F_DIRSET_ADDR, 0x00, 0x20, 0x00, 0x00]), stop=False)

neo = neopixel.NeoPixel(board.NEOPIXEL, 1)

neo.brightness = 0.1

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
led.value = False 

print("NeoPixel Blue")

while True:
    led.value = False
    neo[0] = (0, 0, 255)


"""
`neo_blue`
========================================================
Copyright 2020 Alorium Technology

Contact: info@aloriumtech.com

Description:

This is a very simple CircuitPython program that turns the
Evo M51 NeoPixel blue.

"""
from aloriumtech import board, digitalio, neopixel

neo = neopixel.NeoPixel(board.NEOPIXEL, 1)
neo.brightness = 0.1

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
led.value = False 

print("NeoPixel Blue")

while True:
    led.value = False
    neo[0] = (0, 0, 255)


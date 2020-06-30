"""
`evo_adaio`
========================================================
Copyright 2020 Alorium Technology

Contact: info@aloriumtech.com

Description:

This is an example Evo M51 CircuitPython program that connects to 
Adafruit.io using an Adafruit AirLift FeatherWing. 

This code was leveraged from an Adafruit Learn Guide example that I
cannot seem to remember right now.  However, once I do, I'll be sure to
update this comment to give proper credit. 

"""

import json
import random
import time
import board
import busio

import alorium_evom51 as evo

from digitalio import DigitalInOut, Direction
import neopixel
from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_ntp import NTP

from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# ESP32 Setup
# Enable FPGA Pins
# This is currently clunky but functional. 
# These explicit I2C calls will not be required once an Evo M51 board libary is complete.

# 13
evo.i2c1.writeto(
    0x08, bytes([0x20, evo.D2F_ENSET_ADDR, 0x00, 0x20, 0x00, 0x00]), stop=False
)
evo.i2c1.writeto(
    0x08, bytes([0x20, evo.D2F_DIRSET_ADDR, 0x00, 0x20, 0x00, 0x00]), stop=False
)

# 12
evo.i2c1.writeto(
    0x08, bytes([0x20, evo.D2F_ENSET_ADDR, 0x00, 0x10, 0x00, 0x00]), stop=False
)
evo.i2c1.writeto(
    0x08, bytes([0x20, evo.D2F_DIRSET_ADDR, 0x00, 0x10, 0x00, 0x00]), stop=False
)

# 11
evo.i2c1.writeto(
    0x08, bytes([0x20, evo.D2F_ENSET_ADDR, 0x00, 0x08, 0x00, 0x00]), stop=False
)
evo.i2c1.writeto(
    0x08, bytes([0x20, evo.D2F_DIRCLR_ADDR, 0x00, 0x08, 0x00, 0x00]), stop=False
)

esp32_cs = DigitalInOut(board.D13)  # Connects to D13  - Output to AirLift
esp32_reset = DigitalInOut(board.D12)  # Connects to D12  - Output to Airlift
esp32_ready = DigitalInOut(board.D11)  # Connects to D11  - Input from AirLift

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

status_light = neopixel.NeoPixel(
    board.NEOPIXEL, 1, brightness=0.2
)  

wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

# Set Adafruit IO Username and Key in secrets.py
# (visit io.adafruit.com if you need to create an account,
# or if you need your Adafruit IO key.)
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

# Create an instance of the Adafruit IO HTTP client
io = IO_HTTP(aio_username, aio_key, wifi)

try:
    # Get the test feed from Adafruit IO
    test_feed = io.get_feed("random")
except AdafruitIO_RequestError:
    # If no test feed exists, create one
    test_feed = io.create_new_feed("random")

while True:
    # Send random integer values to the feed
    random_value = random.randint(0, 50)
    print("Sending {0} to random feed - key: {1}".format(random_value, "key"))
    io.send_data(test_feed["key"], random_value)

    time.sleep(20)

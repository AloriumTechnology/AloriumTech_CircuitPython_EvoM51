"""
`busio`
========================================================
Copyright 2020 Alorium Technology. All rights reserved.

Contact: info@aloriumtech.com

Description:

This file is part of the Alorium Technology CiricuitPython Library Bundle
and provides a custom CircuitPython busio library for Evo M51.

"""
import busio

def SPI(clock, MOSI=None, MISO=None):
  busio.SPI(clock[1], MOSI[1], MISO[1])

# TODO: 
# Additional definitions for I2C, UART, and OneWire interfaces
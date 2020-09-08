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
import struct

from aloriumtech import _evo
from aloriumtech import digitalio

class SPI:

  """A 3-4 wire serial protocol

  SPI is a serial protocol that has exclusive pins for data in and out of the
  master.  It is typically faster than :py:class:`~busio.I2C` because a
  separate pin is used to control the active slave rather than a transitted
  address. This class only manages three of the four SPI lines: `!clock`,
  `!MOSI`, `!MISO`. Its up to the client to manage the appropriate slave
  select line. (This is common because multiple slaves can share the `!clock`,
  `!MOSI` and `!MISO` lines and therefore the hardware.)"""

  _SPI = None
  _buffer = bytearray(4)
  _clock = None
  _MOSI = None
  _MISO = None

  def __init__(self, clock, MOSI=None, MISO=None):

    """Construct an SPI object on the given pins.

    ..note:: The SPI peripherals allocated in order of desirability, if possible,
       such as highest speed and not shared use first. For instance, on the nRF52840,
       there is a single 32MHz SPI peripheral, and multiple 8MHz peripherals,
       some of which may also be used for I2C. The 32MHz SPI peripheral is returned
       first, then the exclusive 8MHz SPI peripheral, and finally the shared 8MHz
       peripherals.

    .. seealso:: Using this class directly requires careful lock management.
        Instead, use :class:`~adafruit_bus_device.spi_device.SPIDevice` to
        manage locks.

    .. seealso:: Using this class to directly read registers requires manual
        bit unpacking. Instead, use an existing driver or make one with
        :ref:`Register <register-module-reference>` data descriptors.

    :param ~microcontroller.Pin clock: the pin to use for the clock.
    :param ~microcontroller.Pin MOSI: the Master Out Slave In pin.
    :param ~microcontroller.Pin MISO: the Master In Slave Out pin."""

    # Make FPGA calls to set clock pin as output
    data = 1 << clock[0]
    struct.pack_into("<I", self._buffer, 0, data)
    addr = _evo.D2F_ENSET_ADDR
    _evo.send_evo_write_trans(addr, self._buffer)
    addr = _evo.D2F_DIRSET_ADDR
    _evo.send_evo_write_trans(addr, self._buffer)

    _clock = clock

    if (MOSI != None):

      if (MOSI[0] != 24):
        # Make FPGA calls to set MOSI pin as output
        data = 1 << MOSI[0]
        struct.pack_into("<I", self._buffer, 0, data)
        addr = _evo.D2F_ENSET_ADDR
        _evo.send_evo_write_trans(addr, self._buffer)
        addr = _evo.D2F_DIRSET_ADDR
        _evo.send_evo_write_trans(addr, self._buffer)

      _MOSI = MOSI

    if (MISO != None):

      if (MISO[0] != 23):
        # Make FPGA calls to set MISO pin as input
        data = 1 << MISO[0]
        struct.pack_into("<I", self._buffer, 0, data)
        addr = _evo.D2F_ENSET_ADDR
        _evo.send_evo_write_trans(addr, self._buffer)
        addr = _evo.D2F_DIRCLR_ADDR
        _evo.send_evo_write_trans(addr, self._buffer)

      _MISO = MISO

    # Need to handle each possible combination separately
    if (MOSI == None and MISO == None):
      self._SPI = busio.SPI(_clock[1])
    elif (MOSI == None and MISO != None):
      self._SPI = busio.SPI(_clock[1], MISO=_MISO[1])
    elif (MOSI != None and MISO == None):
      self._SPI = busio.SPI(_clock[1], MOSI=_MOSI[1])
    else:
      self._SPI = busio.SPI(_clock[1], _MOSI[1], _MISO[1])

  @property
  def frequency(self):
    return self._SPI.frequency()

  def deinit(self,):

    """Turn off the SPI bus."""

    # Make FPGA calls to clear clock, mosi, and miso pins

    data = 1 << _clock[0]
    struct.pack_into("<I", self._buffer, 0, data)
    addr = _evo.D2F_DIRCLR_ADDR
    _evo.send_evo_write_trans(addr, self._buffer)

    if (_MOSI != None):

      data = 1 << _MOSI[0]
      struct.pack_into("<I", self._buffer, 0, data)
      addr = _evo.D2F_DIRCLR_ADDR
      _evo.send_evo_write_trans(addr, self._buffer)

    if (_MISO != None):

      data = 1 << _MISO[0]
      struct.pack_into("<I", self._buffer, 0, data)
      addr = _evo.D2F_DIRCLR_ADDR
      _evo.send_evo_write_trans(addr, self._buffer)

    self._SPI.deinit()

  def __enter__(self,):

    """No-op used by Context Managers.
    Provided by context manager helper."""

    self._SPI.__enter__()

  def __exit__(self,):

    """Automatically deinitializes the hardware when exiting a context. See
    :ref:`lifetime-and-contextmanagers` for more info."""

    self._SPI.__exit__()

  def configure(self, *, baudrate=100000, polarity=0, phase=0, bits=8):

    """Configures the SPI bus. The SPI object must be locked.

    :param int baudrate: the desired clock rate in Hertz. The actual clock rate may be higher or lower
      due to the granularity of available clock settings.
      Check the `frequency` attribute for the actual clock rate.
    :param int polarity: the base state of the clock line (0 or 1)
    :param int phase: the edge of the clock that data is captured. First (0)
      or second (1). Rising or falling depends on clock polarity.
    :param int bits: the number of bits per word

    .. note:: On the SAMD21, it is possible to set the baudrate to 24 MHz, but that
       speed is not guaranteed to work. 12 MHz is the next available lower speed, and is
       within spec for the SAMD21.

    .. note:: On the nRF52840, these baudrates are available: 125kHz, 250kHz, 1MHz, 2MHz, 4MHz,
      and 8MHz.
      If you pick a a baudrate other than one of these, the nearest lower
      baudrate will be chosen, with a minimum of 125kHz.
      Two SPI objects may be created, except on the Circuit Playground Bluefruit,
      which allows only one (to allow for an additional I2C object)."""

    self._SPI.configure(baudrate=baudrate, polarity=polarity, phase=phase, bits=bits)

  def try_lock(self,):

    """Attempts to grab the SPI lock. Returns True on success.

    :return: True when lock has been grabbed
    :rtype: bool"""

    return self._SPI.try_lock()

  def unlock(self,):

    """Releases the SPI lock."""

    self._SPI.unlock()

  def write(self, buffer, *, start=0, end=None):

    """Write the data contained in ``buffer``. The SPI object must be locked.
    If the buffer is empty, nothing happens.

    :param bytearray buffer: Write out the data in this buffer
    :param int start: Start of the slice of ``buffer`` to write out: ``buffer[start:end]``
    :param int end: End of the slice; this index is not included. Defaults to ``len(buffer)``"""

    self._SPI.write(buffer, start=start, end=end)

  def readinto(self, buffer, *, start=0, end=None, write_value=0):

    """Read into ``buffer`` while writing ``write_value`` for each byte read.
    The SPI object must be locked.
    If the number of bytes to read is 0, nothing happens.

    :param bytearray buffer: Read data into this buffer
    :param int start: Start of the slice of ``buffer`` to read into: ``buffer[start:end]``
    :param int end: End of the slice; this index is not included. Defaults to ``len(buffer)``
    :param int write_value: Value to write while reading. (Usually ignored.)"""

    if (end != None):
      self._SPI.readinto(buffer, start=start, end=end, write_value=write_value)
    else:
      self._SPI.readinto(buffer, start=start, write_value=write_value)

  def write_readinto(self, buffer_out, buffer_in, *, out_start=0, out_end=None, in_start=0, in_end=None):

    """Write out the data in ``buffer_out`` while simultaneously reading data into ``buffer_in``.
    The SPI object must be locked.
    The lengths of the slices defined by ``buffer_out[out_start:out_end]`` and ``buffer_in[in_start:in_end]``
    must be equal.
    If buffer slice lengths are both 0, nothing happens.

    :param bytearray buffer_out: Write out the data in this buffer
    :param bytearray buffer_in: Read data into this buffer
    :param int out_start: Start of the slice of buffer_out to write out: ``buffer_out[out_start:out_end]``
    :param int out_end: End of the slice; this index is not included. Defaults to ``len(buffer_out)``
    :param int in_start: Start of the slice of ``buffer_in`` to read into: ``buffer_in[in_start:in_end]``
    :param int in_end: End of the slice; this index is not included. Defaults to ``len(buffer_in)``"""

    if (out_end == None and in_end == None):
      self._SPI.write_readinto(buffer_out, buffer_in, out_start=out_start, in_start=in_start)
    elif (out_end == None and in_end != None):
      self._SPI.write_readinto(buffer_out, buffer_in, out_start=out_start, in_start=in_start, in_end=in_end)
    elif (out_end != None and in_end == None):
      self._SPI.write_readinto(buffer_out, buffer_in, out_start=out_start, out_end=out_end, in_start=in_start)
    else:
      self._SPI.write_readinto(buffer_out, buffer_in, out_start=out_start, out_end=out_end, in_start=in_start, in_end=in_end)


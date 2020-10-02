"""
`digitalio`
========================================================
Copyright 2020 Alorium Technology. All rights reserved.

Contact: info@aloriumtech.com

Description:

This file is part of the Alorium Technology CiricuitPython Library Bundle
and provides a custom CircuitPython digitialio library for Evo M51.

"""
import struct

from aloriumtech import _evo

import digitalio
from digitalio import Direction, Pull, DriveMode

class DigitalInOut:
    """Digital input and output

    A DigitalInOut is used to digitally control I/O pins. For analog control of
    a pin, see the :py:class:`analogio.AnalogIn` and
    :py:class:`analogio.AnalogOut` classes."""

    _buffer = bytearray(4)

    def __init__(self, pin):
        """Create a new DigitalInOut object associated with the pin. Defaults to input
        with no pull. Use :py:meth:`switch_to_input` and
        :py:meth:`switch_to_output` to change the direction.

        :param ~microcontroller.Pin pin: The pin to control"""
        self._mask = pin[0]
        self._id = pin[1]
        self._pin = None
        self._direction = None
        data = 1 << self._mask
        struct.pack_into("<I", self._buffer, 0, data)
        if pin[1] == 3:
          pass
        elif pin[1] == 2:
          pass
        elif pin[1] == 1:
          pass
        else:
          addr = _evo.D2F_ENSET_ADDR
          self._pin = digitalio.DigitalInOut(self._id)
          _evo.send_evo_write_trans(addr, self._buffer)

    def deinit(self) -> None:
        """Turn off the DigitalInOut and release the pin for other use."""
        self._mask = pin[0]
        data = 1 << self._mask
        #data = struct.pack("<I", data)
        struct.pack_into("<I", self._buffer, 0, data)
        if self._pin == None:
          pass
        else:
          addr = _evo.D2F_ENCLR_ADDR
          _evo.send_evo_write_trans(addr, self._buffer)

    def soft_deinit(self) -> None:
        """Release the SAMD pin control, but do not reset the FPGA. Useful for configuring a pin for use with an existing library."""
        if self._pin == None:
          pass
        else:
          self._pin.deinit()

    def __enter__(self,) -> DigitalInOut:
        """No-op used by Context Managers."""
        pass

    def __exit__(self,) -> None:
        """Automatically deinitializes the hardware when exiting a context. See
        :ref:`lifetime-and-contextmanagers` for more info."""
        self.deinit()

    def switch_to_output(
        self,
        value: bool = False,
        drive_mode: DriveMode = DriveMode.PUSH_PULL,
        #drive_mode: digitalio.DriveMode = digitalio.DriveMode.PUSH_PULL,
    ) -> None:
        """Set the drive mode and value and then switch to writing out digital
          values.

          :param bool value: default value to set upon switching
          :param ~digitalio.DriveMode drive_mode: drive mode for the output
          """
        data = 1 << self._mask
        struct.pack_into("<I", self._buffer, 0, data)
        if self._id == 3:
          addr = _evo.PORT_Z_DIRSET_ADDR
        elif self._id == 2:
          addr = _evo.PORT_G_DIRSET_ADDR
        elif self._id == 1:
          addr = _evo.PORT_E_DIRSET_ADDR
        else:
          addr = _evo.D2F_DIRSET_ADDR
        _evo.send_evo_write_trans(addr, self._buffer)
        if addr == _evo.D2F_DIRSET_ADDR:
          self._pin.switch_to_output(value, drive_mode)
        # If we subclassed this would be:
        # super().switch_to_output(value, drive_mode)

    def switch_to_input(self, pull: Pull = None) -> None:
        """Set the pull and then switch to read in digital values.

        :param Pull pull: pull configuration for the input

        Example usage::

          import digitalio
          import board

          switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
          switch.switch_to_input(pull=digitalio.Pull.UP)
          # Or, after switch_to_input
          switch.pull = digitalio.Pull.UP
          print(switch.value)"""
        data = 1 << self._mask
        struct.pack_into("<I", self._buffer, 0, data)
        if self._id == 3:
          addr = _evo.PORT_Z_DIRCLR_ADDR
        elif self._id == 2:
          addr = _evo.PORT_G_DIRCLR_ADDR
        elif self._id == 1:
          addr = _evo.PORT_E_DIRCLR_ADDR
        else:
          addr = _evo.D2F_DIRCLR_ADDR
        _evo.send_evo_write_trans(addr, self._buffer)
        if addr == _evo.D2F_DIRSET_ADDR:
          self._pin.switch_to_input(pull)

    @property
    def value(self):
      if self._pin != None:
        return self._pin.value
      else:
        data = 1 << self._mask
        if self._id == 3:
          addr = _evo.PORT_Z_IN_ADDR
        elif self._id == 2:
          addr = _evo.PORT_G_IN_ADDR
        elif self._id == 1:
          addr = _evo.PORT_E_IN_ADDR
        result = _evo.send_evo_read_trans(addr)
        result = struct.unpack("<I", result)
        result = result[0] & data
        if result > 0:
          return True
        else:
          return False
          

    @value.setter
    def value(self, value):
      if self._pin != None:
        self._pin.value = value
      else:
        data = 1 << self._mask
        struct.pack_into("<I", self._buffer, 0, data)
        if value == True:
          if self._id == 3:
            addr = _evo.PORT_Z_OUTSET_ADDR
          elif self._id == 2:
            addr = _evo.PORT_G_OUTSET_ADDR
          elif self._id == 1:
            addr = _evo.PORT_E_OUTSET_ADDR
        else:
          if self._id == 3:
            addr = _evo.PORT_Z_OUTCLR_ADDR
          elif self._id == 2:
            addr = _evo.PORT_G_OUTCLR_ADDR
          elif self._id == 1:
            addr = _evo.PORT_E_OUTCLR_ADDR
        _evo.send_evo_write_trans(addr, self._buffer)

    @property
    def direction(self):
      return self._direction

    # direction: Direction = ...
    # """The direction of the pin.

    # Setting this will use the defaults from the corresponding
    # :py:meth:`switch_to_input` or :py:meth:`switch_to_output` method. If
    # you want to set pull, value or drive mode prior to switching, then use
    # those methods instead."""
    @value.setter
    def direction(self, direction: Direction = Direction.INPUT):
      self._direction = direction
      if self._pin != None:
        self._pin.direction = direction
      if direction == Direction.OUTPUT:
        self.switch_to_output(None)
      elif direction == Direction.INPUT:
        self.switch_to_input(None)
      else:
        pass

    # DriveMode is not available on Evo, simply override and cause an error
    # drive_mode: DriveMode = ...
    # """The pin drive mode. One of:

    # - `digitalio.DriveMode.PUSH_PULL`
    # - `digitalio.DriveMode.OPEN_DRAIN`"""
    @value.setter
    def drive_mode(self, drive_mode: DriveMode = DriveMode.PUSH_PULL):
      raise TypeError("FPGA pins do not allow for DriveMode functionalityal.")

    # Pull is not available on Evo, simply override and cause an error
    # pull: Optional[Pull] = ...
    # """The pin pull direction. One of:

    # - `digitalio.Pull.UP`
    # - `digitalio.Pull.DOWN`
    # - `None`

    # :raises AttributeError: if `direction` is :py:data:`~digitalio.Direction.OUTPUT`."""
    @value.setter
    def pull(self, pull: Pull = Pull.UP):
      raise TypeError("FPGA pins do not allow for Pull functionality.")


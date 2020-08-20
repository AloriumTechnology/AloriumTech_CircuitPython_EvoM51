"""
`neopixel`
========================================================
Copyright 2020 Alorium Technology. All rights reserved.

Contact: info@aloriumtech.com

Description:

This file is part of the Alorium Technology CiricuitPython Library Bundle
and provides a custom CircuitPython neopixel library for Evo M51.

"""

# Evo NeoPixel implementation
import neopixel
import _pixelbuf

from aloriumtech import _evo
from aloriumtech import digitalio

# Pixel color order constants
RGB = "RGB"
"""Red Green Blue"""
GRB = "GRB"
"""Green Red Blue"""
RGBW = "RGBW"
"""Red Green Blue White"""
GRBW = "GRBW"
"""Green Red Blue White"""

class NeoPixel(_pixelbuf.PixelBuf):

  _neopixel = None
  _buffer = bytearray(4)

  def __init__(self, pin, n, *, bpp=3, brightness=1.0, auto_write=True, pixel_order=None):

    if not pixel_order:
      pixel_order = GRB if bpp == 3 else GRBW
    else:
      if isinstance(pixel_order, tuple):
        order_list = [RGBW[order] for order in pixel_order]
        pixel_order = "".join(order_list)

    # Call _pixelbuf __init__
    super().__init__(
      n, brightness=brightness, byteorder=pixel_order, auto_write=auto_write
    )

    # Make FPGA calls to set Neopixel pin as output
    addr = _evo.D2F_ENSET_ADDR
    _evo.send_evo_write_trans(addr, self._buffer)
    addr = _evo.D2F_DIRSET_ADDR
    _evo.send_evo_write_trans(addr, self._buffer)

    # Make call to NeoPixel class
    self._neopixel = neopixel.NeoPixel(pin[1], n, bpp=bpp, brightness=brightness, auto_write=auto_write, pixel_order=pixel_order)

  def deinit(self):
    """Blank out the NeoPixels and release the pin."""
    self._neopixel.fill(0)
    self._neopixel.show()
    self._neopixel.pin.deinit()

  def __enter__(self):
    return self

  def __exit__(self, exception_type, exception_value, traceback):
    self.deinit()

  def __repr__(self):
    return "[" + ", ".join([str(x) for x in self]) + "]"

  @property
  def n(self):
    """
    The number of neopixels in the chain (read-only)
    """
    return self._neopixel.n()

  def write(self):
    self._neopixel.show()

  def _transmit(self, buffer):
    self._neopixel._transmit(buffer)
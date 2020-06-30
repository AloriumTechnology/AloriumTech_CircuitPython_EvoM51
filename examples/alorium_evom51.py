"""
`alorium_evom51`
========================================================
Copyright 2020 Alorium Technology

Contact: info@aloriumtech.com

Description:

This is the start of what may eventually become an Evo M51
specific board library file. 

For now, it just hides some of the FPGA config register defines
separate and keeps the simple examples for Evo a bit cleaner.

"""

import busio
import board

D2F_BASE_ADDR =  0x010
D2F_DIR_ADDR =  D2F_BASE_ADDR + 0x000
D2F_DIRCLR_ADDR =  D2F_BASE_ADDR + 0x001
D2F_DIRSET_ADDR =  D2F_BASE_ADDR + 0x002
D2F_DIRTGL_ADDR =  D2F_BASE_ADDR + 0x003
D2F_EN_ADDR =  D2F_BASE_ADDR + 0x004
D2F_ENCLR_ADDR =  D2F_BASE_ADDR + 0x005
D2F_ENSET_ADDR =  D2F_BASE_ADDR + 0x006
D2F_ENTGL_ADDR =  D2F_BASE_ADDR + 0x007

# Initialize I2C
i2c1 = busio.I2C(board.SCL_1, board.SDA_1, frequency=100000)
while not i2c1.try_lock():
  pass
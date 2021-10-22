"""
`get_evo_info`
========================================================
Copyright 2020 Alorium Technology. All rights reserved.

Contact: info@aloriumtech.com

Description:

This program provides basic information about the Evo M51
board configuration as well as FPGA image, included Xcelertor
Blocks, etc.

"""

import board
import busio

VERBOSE = False

EVO_INFO_MODEL_ADDR = 0x00
EVO_INFO_SERIAL_ADDR = 0x01
EVO_INFO_PART_ADDR = 0x02
EVO_INFO_FTYPE_ADDR = 0x10
EVO_INFO_FSIZE_ADDR = 0x11
EVO_INFO_FSPLY_ADDR = 0x12
EVO_INFO_FFEAT_ADDR = 0x13
EVO_INFO_FPACK_ADDR = 0x14
EVO_INFO_FPINS_ADDR = 0x15
EVO_INFO_FTEMP_ADDR = 0x16
EVO_INFO_FSPED_ADDR = 0x17
EVO_INFO_FOPTN_ADDR = 0x18
EVO_INFO_VER_ADDR = 0x20
EVO_INFO_SVN_ADDR = 0x21
EVO_INFO_XBNUM_ADDR = 0x30

i2c1 = busio.I2C(board.SCL_1, board.SDA_1, frequency=100000)

while not i2c1.try_lock():
    pass

def read_reg(info_addr):
    
    result = bytearray(4)
    
    # Request SVN from Info register
    i2c1.writeto(0x08, bytes([0x20, 0x01, info_addr, 0x00, 0x00, 0x00]))

    # The FPGA will insert data of SVN (0x21) into Info register
    # Request data from Info register, then read result returned from FPGA I2C
    i2c1.writeto_then_readfrom(0x08, bytes([0x20, 0x01]), result)

    return result

print("==================================")
print("Start: get_evo_info")
print("==================================")
results = read_reg(EVO_INFO_MODEL_ADDR)
print(f"Product: {results[3]:c}{results[2]:c}{results[1]:c}{results[0]:c}")
results = int.from_bytes(read_reg(EVO_INFO_PART_ADDR),"little")
print(f"Board Revision: {results}")
print("----------------------------------")
ftype = read_reg(EVO_INFO_FTYPE_ADDR)
fsize = read_reg(EVO_INFO_FSIZE_ADDR)
print(f"FPGA: {ftype[3]:c}{ftype[2]:c}{ftype[1]:c}{ftype[0]:c}{fsize[0]:d}")
# results = read_reg(EVO_INFO_FSIZE_ADDR)
# print(f"FPGA Size: {results[0]:d}")
results = read_reg(EVO_INFO_VER_ADDR)
print(f"FPGA Release: {results[1]:d}{results[0]:d}")
print(f"FPGA SVN: {read_reg(EVO_INFO_SVN_ADDR)[0]}")

print("----------------------------------")

xbs = int.from_bytes(read_reg(EVO_INFO_XBNUM_ADDR),"little")
print(f"Xcelerator Block Config")
print(f'Number of XBs: {xbs:d}')

if (VERBOSE):

    print("----------------------------------")
    print("VERBOSE OUTPUT")
    print("----------------------------------")
    
    results = read_reg(EVO_INFO_MODEL_ADDR)  #  = 0x00  ASCII
    print(f"MODEL: {results[3]:c}{results[2]:c}{results[1]:c}{results[0]:c}")

    results = int.from_bytes(read_reg(EVO_INFO_SERIAL_ADDR),"little") #  = 0x01  INT
    print(f"SRIAL: {results}")

    results = int.from_bytes(read_reg(EVO_INFO_PART_ADDR),"little")   #  = 0x02  INT
    print(f"PART : {results}")

    results = read_reg(EVO_INFO_FTYPE_ADDR)  #  = 0x10  ASCII
    print(f"FTYPE: {results[3]:c}{results[2]:c}{results[1]:c}{results[0]:c}")

    results = int.from_bytes(read_reg(EVO_INFO_FSIZE_ADDR),"little")  #  = 0x11  INT
    print(f"FSIZE: {results}")

    results = read_reg(EVO_INFO_FSPLY_ADDR)  #  = 0x12  ASCII
    print(f"FSPLY: {results[3]:c}{results[2]:c}{results[1]:c}{results[0]:c}")

    results = read_reg(EVO_INFO_FFEAT_ADDR)  #  = 0x13  ASCII
    print(f"FFEAT: {results[3]:c}{results[2]:c}{results[1]:c}{results[0]:c}")

    results = read_reg(EVO_INFO_FPACK_ADDR)  #  = 0x14  ASCII
    print(f"FPACK: {results[3]:c}{results[2]:c}{results[1]:c}{results[0]:c}")

    results = int.from_bytes(read_reg(EVO_INFO_FPINS_ADDR),"little")  #  = 0x15  INT
    print(f"FPINS: {results}")

    results = read_reg(EVO_INFO_FTEMP_ADDR)  #  = 0x16  ASCII
    print(f"FTEMP: {results[3]:c}{results[2]:c}{results[1]:c}{results[0]:c}")
    
    results = int.from_bytes(read_reg(EVO_INFO_FSPED_ADDR),"little")  #  = 0x17  INT
    print(f"SPED : {results}")

    results = read_reg(EVO_INFO_FOPTN_ADDR)  #  = 0x18  ASCII
    print(f"FOPTN: {results[3]:c}{results[2]:c}{results[1]:c}{results[0]:c}")

    results = int.from_bytes(read_reg(EVO_INFO_VER_ADDR),"little")    #  = 0x20  INT
    print(f"VER  : {results}")

    results = int.from_bytes(read_reg(EVO_INFO_SVN_ADDR),"little")    #  = 0x21  INT
    print(f"SVN  : {results}")

print("==================================")
print("End: get_evo_info")
print("==================================")

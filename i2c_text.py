# i2ctest.py
# A brief demonstration of the Raspberry Pi I2C interface, using the Sparkfun
# Pi Wedge breakout board and a SparkFun MCP4725 breakout board:
# https://www.sparkfun.com/products/8736

import smbus2 as smbus
import time

# I2C channel 1 is connected to the GPIO pins
channel = 1

#  MCP4725 defaults to address 0x60
address = 0x25

# Register addresses (with "normal mode" power-down bits)
reg_write_dac = 0xaa

# Initialize I2C (SMBus)
bus = smbus.SMBus(channel)

num = 0

for i in range(0x10000):

    byte1 = i & 0xFF
    data = [byte1]

##    msg = [byte1]

    # Write out I2C command: address, reg_write_dac, msg[0], msg[1]
##    bus.write_i2c_block_data(address, reg_write_dac, data)
    bus.write_byte(address, byte1)
    read_byte = bus.read_byte(address, 1)
    print(i, byte1, read_byte)

# i2ctest.py
# A brief demonstration of the Raspberry Pi I2C interface, using the Sparkfun
# Pi Wedge breakout board and a SparkFun MCP4725 breakout board:
# https://www.sparkfun.com/products/8736

import smbus2 as smbus

# I2C channel 1 is connected to the GPIO pins
channel = 1
i=2

#  MCP4725 defaults to address 0x60
address = 0x25

# Register addresses (with "normal mode" power-down bits)
reg_write_dac = 0xaa

# Initialize I2C (SMBus)
bus = smbus.SMBus(channel)

num = 0

# Create a sawtooth wave 16 times

byte1 = i & 0xFF
data = [byte1]
##    # Create our 12-bit number representing relative voltage
##    voltage = i & 0xfff
##
##    # Shift everything left by 4 bits and separate bytes
##    msg = (voltage & 0xff0) >> 4
##    msg = [msg, (msg & 0xf) << 4]

    # Write out I2C command: address, reg_write_dac, msg[0], msg[1]
read_byte = bus.read_byte(address, 1)
print(i, read_byte)
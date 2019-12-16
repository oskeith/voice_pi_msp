# i2ctest.py
# A brief demonstration of the Raspberry Pi I2C interface, using the Sparkfun
# Pi Wedge breakout board and a SparkFun MCP4725 breakout board:
# https://www.sparkfun.com/products/8736

import smbus2 as smbus

# I2C channel 1 is connected to the GPIO pins
channel = 1

#  MCP4725 defaults to address 0x60
address = 0x25

# Register addresses (with "normal mode" power-down bits)
reg_write_dac = 0xaa

# Initialize I2C (SMBus)
bus = smbus.SMBus(channel)

TXData = [0x00, 0x00, 0x00]
RXData = [None] * 1
num_tx_bytes = len(TXData)
num_rx_bytes = len(RXData)

for i in range(0x10000):

    TXData[0] = i & 0xFF
    TXData[1] = ~TXData[0]
    TXData[2] = ~TXData[1]

    for i2c_idx in range(num_tx_bytes):
        bus.write_byte(address, TXData[i2c_idx])
    for i2c_idx in range(num_rx_bytes):
        RXData[i2c_idx] = bus.read_byte(address)
    print(i, TXData[0], RXData[0])

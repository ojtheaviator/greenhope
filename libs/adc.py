#Only needed for hub

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time

# create the spi bus
spi = busio.SPI(clock=board.SCK_1, MISO=board.MISO_1, MOSI=board.MOSI_1)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.CE0)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
phChan = AnalogIn(mcp, MCP.P0)

liqlev1Chan = AnalogIn(mcp, MCP.P5)
liqlev2Chan = AnalogIn(mcp, MCP.P6)
liqlev3Chan = AnalogIn(mcp, MCP.P7)

def getPh():
    print("ADC: getting ph")
    #calibration/calculation from voltage below
    scaler = 4.2
    offset = 0
    return(phChan.voltage * scaler + offset)

def getLev():
    print("ADC: getting liquid level")
    if liqlev1Chan.voltage > 1.6:
        return(3)
    elif liqlev2Chan.voltage > 1.6:
        return(2)
    elif liqlev1Chan.voltage > 1.6:
        return(1)
    else:
        return(0)

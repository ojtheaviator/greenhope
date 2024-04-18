#Only needed for module

import asyncio
import board
import adafruit_ahtx0

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_ahtx0.AHTx0(i2c)

async def getHum():
    print("AHT20: getting humidity")
    return(sensor.relative_humidity)

async def getTemp():
    print("AHT20: getting temperature")
    return(sensor.temperature)

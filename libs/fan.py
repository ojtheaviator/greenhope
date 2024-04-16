#Only needed for module, TODO

import asyncio
import RPi.GPIO as GPIO

led = 29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)

async def setfan():


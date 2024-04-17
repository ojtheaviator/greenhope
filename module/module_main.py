import asyncio
import sys
import os
import time
from statistics import mean
import RPi.GPIO as GPIO

path1 = os.path.join('..', 'libs')
path2 = os.path.abspath(path1)
sys.path.append(path2)

import aht20
import canlib as can
import ds18
import outputs
#import fan

GPIO.setmode(GPIO.BCM)

heaterOnTemp = 60
heaterOffTemp = 70

def datainit():
    return({"temp":[], "hum":[], "fan":[], "heaterA":[], "heaterB":[]})
def datareset(data):
    data.clear()  # Clears the dictionary in-place
    # Reinitialize data structure after clearing
    for key in datainit():
        data[key] = []

async def transmit(lock, canbus, data, period):
    while True:
        async with lock:
            canbus.transmit(data)
            datareset(data)
        await asyncio.sleep(period)

async def collect_temp(lock, outs, data, period):
    while True:
        #Read temps
        temp = await ds18.read_temp()
        async with lock:
            data["temp"].append((time.strftime('%Y-%m-%d %H:%M:%S'), temp))
        
        #Set heaters
        if mean(temp) < heaterOnTemp:
            outs.heataOn(True)
            outs.heatbOn(True)
            data["heaterA"].append((time.strftime('%Y-%m-%d %H:%M:%S'), "on"))
            data["heaterB"].append((time.strftime('%Y-%m-%d %H:%M:%S'), "on"))
        if mean(temp) > heaterOffTemp:
            outs.heataOn(False)
            outs.heatbOn(False)
            data["heaterA"].append((time.strftime('%Y-%m-%d %H:%M:%S'), "off"))
            data["heaterB"].append((time.strftime('%Y-%m-%d %H:%M:%S'), "off"))
        
        #Wait for next cycle
        await asyncio.sleep(period)

async def collect_hum(lock, data, period):
    while True:
        hum = await aht20.getHum()
        async with lock:
            data["hum"].append((time.strftime('%Y-%m-%d %H:%M:%S'), hum))
        await asyncio.sleep(period)

async def main():
    currentData = datainit()
    cb = can.Can(0x001) #cb = CAN bus
    outs = outputs.Module(initialDutyCycle=50)
    lock = asyncio.Lock()
    tasks = [
        asyncio.create_task(transmit(lock, cb, currentData, 1)),
        asyncio.create_task(collect_temp(lock, outs, currentData, 0.5)),
        asyncio.create_task(collect_hum(lock, currentData, 1))
    ]
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\nExiting with task closure...")
        # Cancel all tasks to ensure clean shutdown
        for task in tasks:
            task.cancel()
        # Wait until all tasks are cancelled.
        await asyncio.gather(*tasks, return_exceptions=True)
        # Any other cleanup code can go here
        cb.close()
        outs.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")

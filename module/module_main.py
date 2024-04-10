import asyncio
import sys
import os

path1 = os.path.join('..', 'testing', 'dummylibs')
path2 = os.path.abspath(path1)
sys.path.append(path2)

import aht20
import canlib as can
import ds18
#import fan


def datainit():
    return({"temp":[], "hum":[], "fan":[]})
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

async def collect_temp(lock, data, period):
    while True:
        temp = await ds18.read_temp()
        async with lock:
            data["temp"].append(temp)
        await asyncio.sleep(period)

async def collect_hum(lock, data, period):
    while True:
        hum = await aht20.getHum()
        async with lock:
            data["hum"].append(hum)
        await asyncio.sleep(period)

async def main():
    currentData = datainit()
    cb = can.Can() #cb = CAN bus
    lock = asyncio.Lock()
    tasks = [
        asyncio.create_task(transmit(lock, cb, currentData, 0.5)),
        asyncio.create_task(collect_temp(lock, currentData, 0.5)),
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

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")

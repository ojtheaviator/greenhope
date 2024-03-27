import sys
import os

path1 = os.path.join('..', 'testing', 'dummylibs')
path2 = os.path.abspath(path1)
sys.path.append(path2)

import aht20
import can
import ds18
import fan


def datainit():
    return({"temp":[], "hum":[], "fan":[]})

async def transmit(canbus, data, freq):
    while True:
        canbus.transmit(data)
        data = datainit()
        await asyncio.sleep(1/freq)

async def collect_temp(data, freq):
    while True:
        data["temp"].append(ds18.read_temp())
        await asyncio.sleep(1/freq)

async def collect_hum(data, freq):
    while True:
        data["temp"].append(ds18.read_temp())
        await asyncio.sleep(1/freq)

async def main():
    currentData = datainit()
    cb = can.Can() #cb = CAN bus
    tasks = []
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

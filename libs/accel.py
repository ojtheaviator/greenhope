import asyncio
import time
import sys
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250


# Create an MPU9250 instance
mpu = MPU9250(
    address_ak=AK8963_ADDRESS,
    address_mpu_master=MPU9050_ADDRESS_68,  # In case the MPU9250 is connected to another I2C device
    address_mpu_slave=None,
    bus=1,
    gfs=GFS_1000,
    afs=AFS_8G,
    mfs=AK8963_BIT_16,
    mode=AK8963_MODE_C100HZ)

# Configure the MPU9250
mpu.configure()

async def getAccel():
    print("MPU9250: getting 1 second of acceleration data")
    magarray = []
    for i in range(100):
        magarray.append(mpu.readMagnetometerMaster())
        await asyncio.sleep(0.01)
    print("MPU9250: got 1 second of acceleration data")
    return(magarray)
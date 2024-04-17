import asyncio
import sys
import os
import time
import pymysql.cursors
from statistics import mean
import RPi.GPIO as GPIO

path1 = os.path.join('..', 'libs')
path2 = os.path.abspath(path1)
sys.path.append(path2)

import adc
import canlib as can
import ds18
import outputs
#import fan

GPIO.setmode(GPIO.BCM)

## Credential
HOST = 'localhost' # MySQL server host DNS
PORT = 3306 # MySQL server port number
USER = 'greenhope' # MySQL account name
PASSWORD = 'Nahwals1234' # Password of the account
DB = 'greenhope' # DB name
TABLE = 'prototype' # table name
## Credential


heaterOnTemp = 60
heaterOffTemp = 70
phLow = 6
phHigh = 8

    #{"temp":[], "hum":[], "fan":[], "heaterA":[], "heaterB":[]}

def querygen(timestamp, sensor, measurement, value):
    return f"INSERT INTO {TABLE} (timestamp,sensor,measurement,value) VALUE('{timestamp}','{sensor}','{measurement}','{value}');"

async def receive(lock, canbus, cursor):
    while True:
        data = await canbus.receive()
        for key in data:
            for datapoint in data[key]:
                sensor = {"temp":"DS18B20", "hum":"AHT20", "fan":"model", "heaterA":"command", "heaterB":"command"}[key]
                measurement = {"temp":"air_temp", "hum":"air_humidity", "fan":"fan_status", "heaterA":"air_heater_state", "heaterB":"heater_state"}[key]
                timestamp = datapoint[0]
                points = datapoint[-1]
                if key == "temp":
                    for i, point in enumrate(points):
                        cursor.execute(querygen(timestamp, sensor, f"{measurement}_{i+1}", point))
                else:
                    cursor.execute(querygen(timestamp, sensor, measurement, points))
        cursor.commit()

async def collect_temp(lock, outs, cursor, period):
    while True:
        #Read temps
        temp = await ds18.read_temp()
        cursor.execute(querygen(time.strftime('%Y-%m-%d %H:%M:%S'), "DS18B20", "water_temperature", temp))
        
        #Set heaters
        if mean(temp) < heaterOnTemp:
            outs.heatOn(True)
            cursor.execute(querygen(time.strftime('%Y-%m-%d %H:%M:%S'), "command", "water_heater_state", "on"))
        if mean(temp) > heaterOffTemp:
            outs.heatOn(False)
            cursor.execute(querygen(time.strftime('%Y-%m-%d %H:%M:%S'), "command", "water_heater_state", "off"))
        
        #Send SQL
        cursor.commit()
        
        #Wait for next cycle
        await asyncio.sleep(period)

async def collect_pH(lock, outs, cursor, period, settlesleep=10):
    while True:
        ph = adc.getPh()
        cursor.execute(querygen(time.strftime('%Y-%m-%d %H:%M:%S'), "ADC", "pH_reading", ph))
        cursor.commit()
        if ph > phHigh:
            outs.phDown()
            await asyncio.sleep(settlesleep)
        if ph < phLow:
            outs.phUp()
            await asyncio.sleep(settlesleep)
        await asyncio.sleep(period)

async def main():
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, port=PORT) # make a connection to MySQL server
    cursor = connection.cursor() # Open cursur to execute SQL query
    
    cb = can.Can(0x000) #cb = CAN bus
    outs = outputs.Hub()
    lock = asyncio.Lock()
    tasks = [
        asyncio.create_task(receive(lock, cb, cursor)),
        asyncio.create_task(collect_temp(lock, outs, cursor, 0.5)),
        asyncio.create_task(collect_pH(lock, outs, cursor, 1))
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
        connection.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")

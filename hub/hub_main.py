import asyncio
import sys
import os
import datetime
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

print("Imports done!")

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

async def receive(lock, canbus, cursor, connection):
    while True:
        data = await canbus.receive()
        print("CAN message received")
        for key in data:
            for datapoint in data[key]:
                sensor = {"temp":"DS18B20", "hum":"AHT20", "fan":"model", "heaterA":"command", "heaterB":"command"}[key]
                measurement = {"temp":"air_temp", "hum":"air_humidity", "fan":"fan_status", "heaterA":"heaterA", "heaterB":"heaterB"}[key]
                timestamp = datapoint[0]
                points = datapoint[-1]
                if key == "temp":
                    for i, point in enumerate(points):
                        cursor.execute(querygen(timestamp, sensor, f"{measurement}_{i+1}", point))
                else:
                    cursor.execute(querygen(timestamp, sensor, measurement, points))
        connection.commit()

async def collect_temp(lock, outs, cursor, connection, period):
    while True:
        #Read temps
        temp = await ds18.read_temp()
        print("temps gotten")
        cursor.execute(querygen(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), "DS18B20", "water_temperature", mean(temp)))
        
        #Set heaters
        '''if mean(temp) < heaterOnTemp:
            outs.heatOn(True)
            cursor.execute(querygen(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), "command", "water_heater_state", "on"))
        if mean(temp) > heaterOffTemp:
            outs.heatOn(False)
            cursor.execute(querygen(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), "command", "water_heater_state", "off"))'''
        
        #Send SQL
        connection.commit()
        
        #Wait for next cycle
        await asyncio.sleep(period)

async def lightcontrol(outs, ontime=(8, 5), offtime=(0, 5)):
    while True:
        m_ontime = ontime[1] + 60 * ontime[0]
        m_offtime = offtime[1] + 60 * offtime[0]
        curTime = datetime.datetime.now().time()
        curHr = curTime.hour
        curMin = curTime.minute
        m_cur = curMin + 60 * curHr
        curSec = curTime.second
        if m_offtime < m_ontime:
            m_offtime += 24*60
        if m_cur < m_ontime:
            m_cur += 24*60
        if (m_cur > m_ontime) and (m_cur < m_offtime):
            outs.lightsOn(True)
        else:
            outs.lightsOn(False)
        await asyncio.sleep(60-curSec)


async def collect_pH(lock, outs, cursor, connection, period, settlesleep=10):
    while True:
        ph = adc.getPh()
        print(f"ph gotten: indicated {ph}")
        cursor.execute(querygen(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), "ADC", "pH_reading", ph))
        print("query queued")
        connection.commit()
        print("query committed")
        '''
        if ph > phHigh:
            outs.phDown()
            await asyncio.sleep(settlesleep)
        if ph < phLow:
            outs.phUp()
            await asyncio.sleep(settlesleep)
        '''
        await asyncio.sleep(period)

async def main():
    print("main starting")
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, port=PORT) # make a connection to MySQL server
    
    print("Complete: connected to SQL database")

    cursor = connection.cursor() # Open cursur to execute SQL query

    cb = can.Can(0x000) #cb = CAN bus
    
    print("Complete: set up canbus")

    outs = outputs.Hub()
    outs.pumpOn(True)
    outs.lightsOn(True)
    outs.heatOn(True)

    print("Complete: set up outputs")

    lock = asyncio.Lock()
    tasks = [
        asyncio.create_task(receive(lock, cb, cursor, connection)),
        asyncio.create_task(collect_temp(lock, outs, cursor, connection, 30)),
        asyncio.create_task(collect_pH(lock, outs, cursor, connection, 100)),
        asyncio.create_task(lightcontrol(outs, (8, 5), (0, 21)))
    ]
    print("Gathering tasks...")
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
    finally:
        if connection:
            connection.close()
        if cb:
            cb.close()
        if outs:
            outs.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")

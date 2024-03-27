import asyncio
import glob

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

async def read_temp_raw():
    # Use asyncio.to_thread to run the blocking file I/O operations in a separate thread
    with open(device_file, 'r') as f:
        lines = await asyncio.to_thread(f.readlines)
    return lines

async def read_temp():
    lines = await read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        await asyncio.sleep(0.2)  # Replace time.sleep with asyncio.sleep
        lines = await read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

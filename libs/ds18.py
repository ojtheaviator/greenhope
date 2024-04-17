#Both hub and module!

import asyncio
import glob
import subprocess



all_device_folders = subprocess.check_output(['ls', '/sys/bus/w1/devices/']).decode("utf-8").split()
ds18b20_folders = [i for i in all_device_folders if i[0:3]=="28-"]

base_dir = '/sys/bus/w1/devices/'
device_folders = [glob.glob(base_dir + i)[0] for i in ds18b20_folders]
device_files = [i + '/w1_slave' for i in device_folders]

async def read_temp_raw():
    # Use asyncio.to_thread to run the blocking file I/O operations in a separate thread    
    all_lines = []
    for device_file in device_files:
        with open(device_file, 'r') as f:
            lines = await asyncio.to_thread(f.readlines)
            all_lines.append(lines)
    return all_lines

async def read_temp():
    all_lines = await read_temp_raw()
    temps = []
    for lines in all_lines:
        while lines[0].strip()[-3:] != 'YES':
            await asyncio.sleep(0.2)  # Replace time.sleep with asyncio.sleep
            lines = await read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            temps.append(temp_f)
    return temps

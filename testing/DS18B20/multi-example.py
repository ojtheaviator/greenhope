# SPDX-FileCopyrightText: 2019 Mikey Sklar for Adafruit Industries
#
# SPDX-License-Identifier: MIT



'''
test = subprocess.check_output(['ls', '/sys/bus/w1/devices/']).decode("utf-8")
test
'28-0000003106b0\n28-00000032027f\nw1_bus_master1\n'
type(test)
<class 'str'>
splittest = test.split()
splittest
['28-0000003106b0', '28-00000032027f', 'w1_bus_master1']
'''

import glob
import time
import subprocess

all_device_folders = subprocess.check_output(['ls', '/sys/bus/w1/devices/']).decode("utf-8").split()
ds18b20_folders = [i for i in all_device_folders if i[0:3]=="28-"]

base_dir = '/sys/bus/w1/devices/'
device_folders = [glob.glob(base_dir + i)[0] for i in ds18b20_folders]
device_files = [i + '/w1_slave' for i in device_folders]

def read_temps_raw():
    all_lines = []
    for device_file in device_files:
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        all_lines.append(lines)
    return all_lines

def read_temps():
    all_lines = read_temps_raw()
    temps = []
    for lines in all_lines:
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            temps.append([temp_c, temp_f])
    return temps

while True:
    print(read_temps())
    time.sleep(1)

"""Read temperature sensors and write them to the temperature file"""
#!/usr/bin/python3
import os
import glob
import time
import datetime
MAX_TEMP = 150.0
TIME_BETWEEN_READINGS = 14.0
WAIT_DELAY = .2
WRITE_APPEND = "a"
OVERWRITE = "w"
USERNAME = os.getlogin()
BASE_DIR = '/sys/bus/w1/devices/'

def read_temp_raw(temp_device_file):
    """read the device and return its raw value"""
    lines = ""
    with open(temp_device_file, 'r', encoding="utf-8") as temp_f:
        lines = temp_f.readlines()
    return lines

def read_temp(temp_device_file):
    """Read the device, discard excess info, and return temp in fahrenheit"""
    lines = read_temp_raw(temp_device_file)
    # IF unsecessful read, try one more time
    if lines[0].strip()[-3:] != 'YES':
        time.sleep(WAIT_DELAY)
        lines = read_temp_raw(temp_device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        if temp_f > MAX_TEMP: # Send back a value that won't throw off averages too much
            temp_f = 70.0
        return temp_f
    # If things go wrong, send back an extreme value
    return -100.0

device_files = []
if len(glob.glob(BASE_DIR+'28*')) > 0:
    for therm in glob.glob(BASE_DIR+'28*'):
        device_files.append(therm + '/w1_slave')

if len(device_files) > 0:
    while True:
        line = ""
        date_string = datetime.datetime.now().strftime("%Y-%m-%d")
        tempf_directory = f"/home/{USERNAME}/ghcontrol/temperature_files/tempf"
        filename = f"{tempf_directory}/{date_string}.tempf"
        filename_current = f"{tempf_directory}/current.tempf"
        line += datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for device_file in device_files:
            line += f" {read_temp(device_file):.1f}"
        line += "\n"
        with open(filename, WRITE_APPEND, encoding="utf-8") as f:
            f.write(line)
        with open(filename_current, OVERWRITE, encoding="utf-8") as f:
            f.write(line)
        time.sleep(TIME_BETWEEN_READINGS)
print("No temperature sensors or something went wrong inside read loop")

import os
import glob
import time
WAIT_DELAY = .2

def read_temp_raw(device_file):
   print(device_file)
   lines = ""
   with open(device_file, 'r') as f:
      lines = f.readlines()
   return lines

def read_temp(device_file):
   lines = read_temp_raw(device_file)
   print(lines)
   if lines[0].strip()[-3:] != 'YES':
      time.sleep(WAIT_DELAY)
      lines = read_temp_raw(device_file)
      print(lines)
      equals_pos = lines[1].find('t=')
      if equals_pos != -1:
         temp_string = lines[1][equals_pos+2:]
         temp_c = float(temp_string) / 1000.0
         temp_f = temp_c * 9.0 / 5.0 + 32.0
         return temp_c, temp_f
   # If things go wrong
   return -100.0,-100.0

base_dir = '/sys/bus/w1/devices/'
device_files = []
if len(glob.glob(base_dir+'28*')) > 0:
   for therm in glob.glob(base_dir + '28*'):
      device_files.append(therm + '/w1_slave')


if len(device_files) > 0:
   while True:
      for device_file in device_files:
         print(read_temp(device_file))
      time.sleep(1)
print("No temperature sensors or something went wrong inside read loop")

#!/usr/bin/python3
import os
import glob
import time
import datetime
TIME_BETWEEN_READINGS = 14.0
WAIT_DELAY = .2
WRITE_APPEND = "a"

def read_temp_raw(device_file):
   lines = ""
   with open(device_file, 'r') as f:
      lines = f.readlines()
   return lines

def read_temp(device_file):
   lines = read_temp_raw(device_file)
   # IF unsecessful read, try one more time
   if lines[0].strip()[-3:] != 'YES':
      time.sleep(WAIT_DELAY)
      lines = read_temp_raw(device_file)
   equals_pos = lines[1].find('t=')
   if equals_pos != -1:
      temp_string = lines[1][equals_pos+2:]
      #print(temp_string)
      temp_c = float(temp_string) / 1000.0
      temp_f = temp_c * 9.0 / 5.0 + 32.0
      return temp_f
   # If things go wrong, send back an extreme value
   return -100.0

username = os.getlogin()
base_dir = '/sys/bus/w1/devices/'
device_files = []
if len(glob.glob(base_dir+'28*')) > 0:
   for therm in glob.glob(base_dir + '28*'):
      device_files.append(therm + '/w1_slave')

if len(device_files) > 0:
   while True:
      line = ""
      filename = "/home/%s/ghcontrol/temperature_files/tempf/%s.tempf" % (username, datetime.datetime.now().strftime("%Y-%m-%d"))
      line += datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      for device_file in device_files:
         line += " %.1f" % read_temp(device_file)
      line += "\n"
      with open(filename, WRITE_APPEND) as f:
         f.write(line)
      time.sleep(TIME_BETWEEN_READINGS)
print("No temperature sensors or something went wrong inside read loop")


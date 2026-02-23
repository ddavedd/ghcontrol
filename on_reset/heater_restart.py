#!/usr/bin/python3
import os
from os.path import isfile, join
username = os.getlogin()
heater_on_scripts = []
with open("/home/%s/ghcontrol/on_reset/heater_enable_on_restart.txt" % username) as f:
   enable = int(f.read())
   if enable == 1:
      scripts_directory = "/home/%s/ghcontrol/scripts" % username
      files = [f for f in os.listdir(scripts_directory) if isfile(join(scripts_directory,f))]
      for f in files:
         if f.startswith("Heater") and f.endswith("Enable_On.sh"):
            heater_on_scripts.append(f)
for f in heater_on_scripts:
   print("Running script " + f)
   os.system("/home/%s/ghcontrol/scripts/%s" % (username, f))

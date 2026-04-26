"""After a reboot, heaters should be enabled automatically if defined by heater_enable_on_restart"""
#!/usr/bin/python3
import os
from os.path import isfile, join
username = os.getlogin()
SCRIPTS_DIRECTORY = "/home/{username}/ghcontrol/scripts"
heater_on_scripts = []
with open(f"/home/{username}/ghcontrol/on_reset/heater_enable_on_restart.txt", encoding="utf-8") as f:
    enable = int(f.read())
    if enable == 1:
        files = [f for f in os.listdir(SCRIPTS_DIRECTORY) if isfile(join(SCRIPTS_DIRECTORY,f))]
        for f in files:
            if f.startswith("Heater") and f.endswith("Enable_On.sh"):
                heater_on_scripts.append(f)
for heater_script in heater_on_scripts:
    print(f"Running script {heater_script}")
    os.system(f"/home/{username}/ghcontrol/scripts/{heater_script}")

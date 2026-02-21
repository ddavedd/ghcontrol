#!/usr/bin/python3
with open("heater_enable_on_restart.txt") as f:
    enable = int(f.read())
    if enable == 1:
        

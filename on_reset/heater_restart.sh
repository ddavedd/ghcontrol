#! /usr/bin/bash
echo "Running Heater Restart"
/usr/bin/python3 /home/$(/usr/bin/id -un)/ghcontrol/on_reset/heater_restart.py

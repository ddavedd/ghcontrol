#! /usr/bin/bash
echo "Running control temperature"
/usr/bin/python3 /home/$(/usr/bin/id -un)/ghcontrol/on_reset/control_temp.py

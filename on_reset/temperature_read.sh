#! /usr/bin/bash
echo "Running temperature read"
/usr/bin/python3 /home/$(/usr/bin/id -un)/ghcontrol/on_reset/temperature_read.py

#! /usr/bin/bash
echo $(/usr/bin/date +'%F %T') "Running temperature read"
/usr/bin/python3 /home/$(/usr/bin/id -un)/ghcontrol/on_reset/temperature_read.py
echo $(/usr/bin/date +'%F %T') "Ending temperature read"

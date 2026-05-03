#! /usr/bin/bash
echo $(/usr/bin/date +'%F %T') "Running Buttons Setup"
/usr/bin/python3 /home/$(/usr/bin/id -un)/ghcontrol/on_reset/buttons_setup.py
echo $(/usr/bin/date +'%F %T') "Buttons Setup Close"

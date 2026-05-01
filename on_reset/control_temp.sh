#! /usr/bin/bash
USER=$(/usr/bin/id -un)
DATE=$(/usr/bin/date +'%F %T')
echo $DATE "Running control temperature"
echo $USER
{/usr/bin/python3 /home/$USER/ghcontrol/on_reset/control_temp.py} >> /home/$USER/ghcontrol/logs/$DATE.$USER.control.log

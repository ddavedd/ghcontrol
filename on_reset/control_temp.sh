#! /usr/bin/bash
echo $(/usr/bin/date +'%F %T') "Running control temperature"
USER=$(/usr/bin/id -un)
/usr/bin/python3 /home/$USER/ghcontrol/on_reset/control_temp.py &>> /home/$USER/ghcontrol/logs/$(/usr/bin/date +'%F %T').$USER.control.log

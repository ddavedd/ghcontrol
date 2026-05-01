#! /usr/bin/bash
USER=$(/usr/bin/id -un)
DATE=$(/usr/bin/date +'%F %T')
LOG_FILE_CONTROL=$(/home/$USER/ghcontrol/logs/$DATE.$USER.control.log)
echo $DATE $USER "Running control temperature"
echo "Log file for control is " $LOG_FILE_CONTROL
{/usr/bin/python3 /home/$USER/ghcontrol/on_reset/control_temp.py} >> $LOG_FILE_CONTROL

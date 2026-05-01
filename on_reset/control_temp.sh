#! /usr/bin/bash
USER=$(/usr/bin/id -un)
DATETIME=$(/usr/bin/date +'%F %T')
DATE=$(/usr/bin/date +'%F')
LOG_FILE_CONTROL=/home/$USER/ghcontrol/logs/$DATE.$USER.control.log
echo $DATETIME $USER "Running control temperature"
echo $LOG_FILE_CONTROL "Log file for control is " $LOG_FILE_CONTROL
/usr/bin/python3 /home/$USER/ghcontrol/on_reset/control_temp.py >> $LOG_FILE_CONTROL

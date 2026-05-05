#! /usr/bin/bash
CONTROL_FILE="control_temp.sh"
TIME=$(date +%H:%M:%S)
DATE=$(date +%Y-%m-%d)
USER=$(id -un)
LOGFILE=/home/$USER/ghcontrol/logs/$DATE.restart.log
if pgrep -f buttons_setup.py; then echo "$TIME $CONTROL_FILE still running"; else echo "$TIME Restarting $CONTROL_FILE"; fi >> $LOGFILE

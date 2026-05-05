#! /usr/bin/bash
BUTTONS_FILE="buttons_setup.sh"
TIME=$(date +%H:%M:%S)
DATE=$(date +%Y-%m-%d)
USER=$(id -un)
LOGFILE=/home/$USER/ghcontrol/logs/$DATE.restart.log
if pgrep -f $BUTTONS_FILE; then echo "$TIME $BUTTONS_FILE still running"; else echo "$TIME Restarting $BUTTONS_FILE"; fi >> $LOGFILE

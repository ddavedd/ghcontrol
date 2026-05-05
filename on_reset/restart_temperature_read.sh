#! /usr/bin/bash
TEMPERATURE_FILE="temperature_read.sh"
TIME=$(date +%H:%M:%S)
DATE=$(date +%Y-%m-%d)
USER=$(id -un)
LOGFILE=/home/$USER/ghcontrol/logs/$DATE.restart.log
if pgrep -f buttons_setup.py; then echo "$TEMPERATURE_FILE still running"; else echo "$TIME Restarting $TEMPERATURE_FILE"; fi >> $LOGFILE

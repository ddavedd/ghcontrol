#! /usr/bin/bash
TEMPERATURE_FILE="temperature_read.sh"
TIME=$(date +%H:%M:%S)
DATE=$(date +%Y-%m-%d)
USER=$(id -un)
FULL_PATH_FILE=/home/$USER/ghcontrol/on_reset/$TEMPERATURE_FILE
LOGFILE=/home/$USER/ghcontrol/logs/$DATE.restart.log
if pgrep -f $TEMPERATURE_FILE; then
    echo "$TIME $TEMPERATURE_FILE still running"
else
    echo "$TIME Restarting $TEMPERATURE_FILE"
    /usr/bin/nohup /usr/bin/bash $FULL_PATH_FILE &
fi >> $LOGFILE

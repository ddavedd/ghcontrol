#! /usr/bin/bash
CONTROL_FILE="control_temp.sh"
TIME=$(date +%H:%M:%S)
DATE=$(date +%Y-%m-%d)
USER=$(id -un)
FULL_PATH_FILE=/home/$USER/ghcontrol/on_reset/$CONTROL_FILE
LOGFILE=/home/$USER/ghcontrol/logs/$DATE.restart.log
if pgrep -f $CONTROL_FILE; then 
    echo "$TIME $CONTROL_FILE still running"
else
    echo "$TIME Restarting $CONTROL_FILE"
    /usr/bin/nohup /usr/bin/bash $FULL_PATH_FILE &
fi >> $LOGFILE

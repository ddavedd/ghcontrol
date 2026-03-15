#!/bin/bash
USER=$(id -un)
echo UPLOAD_DAILY_REPORT
FARM_PW=$(cat /home/$USER/ghcontrol/report_upload/.ftp_pass)
LATEST_LOG=$(ls -t /home/$USER}/ghcontrol/logs/ | head -1)
LATEST_PNG=$(ls -t /home/$USER/ghcontrol/temperature_files/png/ | head -1)
ftp -nvi ftp.thefarmwestmont.com << END_SCRIPT
user thefarmwestmontcom $FARM_PW
cd gh
mkdir 2026
cd 2026
mkdir $USER
cd $USER
lcd /home/$USER/ghcontrol/report_upload/
put index.html
mkdir graphs
cd graphs
lcd /home/$USER/ghcontrol/temperature_files/png/
put $LATEST_PNG
cd ..
lcd /home/$USER/ghcontrol/logs/
mkdir reports
cd reports
put $LATEST_LOG
bye
END_SCRIPT

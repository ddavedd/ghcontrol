#!/bin/bash
USER=$(id -un)
echo UPLOAD_ALL_REPORTS
FARM_PW=$(cat /home/$USER/ghcontrol/report_upload/.ftp_pass)

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
mput *.png
cd ..
lcd /home/$USER/ghcontrol/logs/
mkdir reports
cd reports
mput *.log
bye
END_SCRIPT

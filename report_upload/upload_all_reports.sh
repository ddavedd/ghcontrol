#!/bin/bash
echo UPLOAD_ALL_REPORTS
FARM_PW=$(cat /home/${whoami}/ghcontrol/report_upload/.ftp_pass)

ftp -nvi ftp.thefarmwestmont.com << END_SCRIPT
user thefarmwestmontcom $FARM_PW
cd gh
mkdir 2026
cd 2026
mkdir ${whoami}
cd ${whoami}
lcd /home/${whoami}/ghcontrol/report_upload/
put index.html
mkdir graphs
cd graphs
lcd /home/${whoami}/ghcontrol/temperature_files/png/
mput *.png
cd ..
lcd /home/${whoami}/ghcontrol/logs/
mkdir reports
cd reports
mput *.log
bye
END_SCRIPT

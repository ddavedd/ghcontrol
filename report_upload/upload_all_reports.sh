#!/bin/bash
FARM_PW=$(cat /home/$USER/ghcontrol/report_upload/.ftp_pass)
cd /home/${USER}/ghcontrol/report_upload
ftp -nvi ftp.thefarmwestmont.com << END_SCRIPT
user thefarmwestmontcom $FARM_PW
cd gh
mkdir 2026
cd 2026
mkdir ${USER}
cd ${USER}
lcd graphs
mkdir graphs
cd graphs
put *.png
cd ..
lcd ..
lcd reports
mkdir reports
cd reports
put *.report
bye
END_SCRIPT

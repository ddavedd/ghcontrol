#!/bin/bash
FARM_PW=$(cat /home/$USER/ghcontrol/report_upload/.ftp_pass)
cd /home/${USER}/ghcontrol/temperature_files/png/
ftp -nvi ftp.thefarmwestmont.com << END_SCRIPT
user thefarmwestmontcom $FARM_PW
cd gh
mkdir 2026
cd 2026
mkdir ${USER}
cd ${USER}
mkdir graphs
cd graphs

ls
bye
END_SCRIPT

#!/bin/bash
FARM_PW=$(cat /home/$USER/ghcontrol/report_upload/.ftp_pass)
cd /home/${USER}/ghcontrol/report_upload
#a=(*)
#cp ${a[@]: -1} westchestertoday.html
ftp -nvi ftp.thefarmwestmont.com << END_SCRIPT
user thefarmwestmontcom $FARM_PW
cd gh
mkdir 2026
cd 2026
ls
bye
END_SCRIPT

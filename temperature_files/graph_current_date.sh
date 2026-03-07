#! /usr/bin/bash
date_current=$(date +"%Y-%m-%d")
/usr/bin/python3 /home/$USER/ghcontrol/temperature_files/temp_plot.py $date_current.tempf

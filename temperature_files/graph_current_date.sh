#! /usr/bin/bash
date_current=$(date +"%Y-%m-%d")
USER=$(id -un)
/usr/bin/python3 /home/$USER/ghcontrol/temperature_files/temp_plot.py /home/$USER/ghcontrol/temperature_files/tempf/$date_current.tempf
cp /home/$USER/ghcontrol/temperature_files/png/$date_current.png /home/$USER/ghcontrol/temperature_files/png/current.png

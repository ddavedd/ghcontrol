for f in /home/$USER/ghcontrol/temperature_files/tempf/*.tempf
do
   echo $f
   /usr/bin/python3 /home/$USER/ghcontrol/temperature_files/temp_plot.py $f
done

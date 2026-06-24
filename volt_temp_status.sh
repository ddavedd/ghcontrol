#! /usr/bin/bash
USER=$(id -un)
VOLTAGE=$(vcgencmd pmic_read_adc EXT5V_V)
TEMP_C=$(vcgencmd measure_temp)
/home/$USER/ghcontrol/scripts/log_event.sh "Voltage $VOLTAGE Volts, Temp(C) $TEMP_C"


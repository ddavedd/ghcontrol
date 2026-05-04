#! /usr/bin/bash
USER=$(id -un)
/usr/bin/python3 /home/$USER/ghcontrol/read_status_on.py > /home/$USER/ghcontrol/current_status.txt
/home/$USER/ghcontrol/scripts/log_event.sh "$(cat /home/$USER/ghcontrol/current_status.txt)"

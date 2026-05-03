ssh halfsouth@halfsouth.lan ./ghcontrol/status.sh &>> /home/$USER/ghcontrol/status.log
cat /home/$USER/ghcontrol/status.log | grep Status: >> /home/$USER/ghcontrol/status.out
/home/$USER/ghcontrol/scripts/log_event.sh "$(cat /home/$USER/ghcontrol/status.out)"
#rm /home/$USER/ghcontrol/status.log
#rm /home/$USER/ghcontrol/status.out

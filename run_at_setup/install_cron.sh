#! /usr/bin/bash
# Assemble Cron parts
/usr/bin/bash /home/$USER/ghcontrol/cron/assemble_cron_file.sh
# Install crontab file
crontab /home/$USER/ghcontrol/cron/gh.cron

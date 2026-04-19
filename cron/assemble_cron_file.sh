cd /home/$USER/ghcontrol/cron
cat cron_start.cron.template cron_reboot.cron.template cron_status.cron.template cron_graphs_and_report.cron.template cron_haf_schedule.cron.template > assembled.cron
CRON_LOG=/home/$USER/ghcontrol/logs/$(date +"%F").cron.log
USERNAME=$(id -un)
sed "s/USERNAME/$USERNAME/g" assembled.cron > username_replaced.cron
sed "s/CRON_LOG/$CRON_LOG/g" username_replaced.cron > gh.cron

cd /home/$USER/ghcontrol/cron
cat cron_start.cron.template cron_reboot.cron.template cron_status.cron.template cron_graphs_and_report.cron.template cron_haf_schedule.cron.template > assembled.cron
CRON_LOG='/home/USERNAME/ghcontrol/logs/$(/usr/bin/date +%F).cron.log'
sed "s#CRON_LOG#$CRON_LOG#g" assembled.cron > cron_log_replaced.cron
USERNAME="$(id -un)"
sed "s/USERNAME/$USERNAME/g" cron_log_replaced.cron > gh.cron

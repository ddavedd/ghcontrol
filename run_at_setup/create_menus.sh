/home/${USER}/ghcontrol/run_at_setup/clean_scripts_directory_desktop_entries.sh
/usr/bin/python3 /home/${USER}/ghcontrol/run_at_setup/create_scripts_from_connections.py
/usr/bin/python3 /home/${USER}/ghcontrol/run_at_setup/get_status.template.py
sed "s/USERNAME/${USER}/g" /home/${USER}/ghcontrol/templates/log_event.sh.template > /home/${USER}/ghcontrol/scripts/log_event.sh
/home/${USER}/ghcontrol/run_at_setup/make_scripts_executable.sh

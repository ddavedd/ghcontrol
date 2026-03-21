/home/${USER}/ghcontrol/templates/clean_scripts_directory_desktop_entries.sh
/usr/bin/python3 /home/${USER}/ghcontrol/templates/create_scripts_from_connections.py
/usr/bin/python3 /home/${USER}/ghcontrol/templates/get_status.template.py
sed "s/USERNAME/${USER}/g" /home/${USER}/ghcontrol/templates/log_event.sh.template > /home/${USER}/ghcontrol/scripts/log_event.sh
/home/${USER}/ghcontrol/templates/make_scripts_executable.sh

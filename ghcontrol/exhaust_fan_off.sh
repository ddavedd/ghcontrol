#! /usr/bin/bash
/home/USERNAME/ghcontrol/log_event.sh "Exhaust Fan Off"
/usr/local/bin/3relind 0 write 1 0
/usr/local/bin/3relind 0 write 2 0

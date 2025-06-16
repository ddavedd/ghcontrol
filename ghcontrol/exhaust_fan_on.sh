#! /usr/bin/bash
/home/USERNAME/ghcontrol/log_event.sh "Exhaust Fan On"
/usr/local/bin/3relind 0 write 1 1
/usr/local/bin/3relind 0 write 2 1

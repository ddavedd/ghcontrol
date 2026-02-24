#! /usr/bin/python3
import os
import subprocess
username = os.getlogin()
for number in [3,8]:
   output = subprocess.check_output(["/usr/local/bin/%irelind"%number,"-list"], text=True)
   #output = "2 board(s) detected\nId: 1 0\n"
   boards = output.split("\n")[1].split(" ")[1:]
   text = ""
   for b in boards:
      text += "/home/%s/ghcontrol/scripts/log_event.sh \"/usr/local/bin/%irelind %s read: $(/usr/local/bin/%irelind %s read)\"\n" % (username, number, b, number, b)
   with open("/home/%s/ghcontrol/scripts/get_status_%i.sh" % (username, number), "w", encoding="utf-8") as f:
      f.write(text)


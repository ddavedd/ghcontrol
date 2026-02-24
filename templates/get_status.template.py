#! /usr/bin/python3
import os
username = os.getlogin()
for number in [3,8]:
   #output = os.system("/usr/bin/%irelind -list" % number)
   output = "2 board(s) detected\nId: 1 0\n"
   boards = output.split("\n")[1].split(" ")[1:]
   text = ""
   for b in boards:
      text += "/home/%s/ghcontrol/log_event.sh \"/usr/local/bin/%irelind %s read: $(/usr/local/bin/%irelind %s read)\"\n" % (username, number, b, number, b)
   print(text)

""" The template for get status shell file, used to read the status of 3relind & 8relind boards Sequent Microsystems"""
#! /usr/bin/python3
import os
import subprocess
username = os.getlogin()

for number in [3,8]:
    output = subprocess.check_output([f"/usr/local/bin/{number}relind","-list"], text=True)
    #output = "2 board(s) detected\nId: 1 0\n"
    boards = output.split("\n")[1].split(" ")[1:]
    text = ""
    for b in boards:
        text += f"/home/{username}/ghcontrol/scripts/log_event.sh \"/usr/local/bin/{number}irelind {b} read: $(/usr/local/bin/{number}relind {b} read)\"\n"
    with open(f"/home/{username}/ghcontrol/scripts/get_status_{number}.sh", "w", encoding="utf-8") as f:
        f.write(text)

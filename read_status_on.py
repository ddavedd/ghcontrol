"""Using the map we created at setup, print the status of relays that are on"""
import time
import os
import subprocess
import sys
username = os.getlogin()

with open(f"/home/{username}/ghcontrol/maps/{username}_comp_read.map", encoding="utf-8") as f:
    connections = f.readlines()

if len(connections)>0:
    total_string = "Status: "
    for c in connections:
        x = c.strip().split(',')
        relay_board = int(x[0])
        board_number = int(x[1])
        relay_number = int(x[2])
        relay_name = x[3]
        relay_on_off = x[5]
        mread = x[4]
        if mread == "True":
            read_string = "mread"
            time.sleep(.25)
        else:
            read_string = "read"
        print(x,file=sys.stderr)
        print(read_string,file=sys.stderr)
        if int(subprocess.check_output(f"{relay_board}relind {board_number} {read_string} {relay_number}", shell=True)) == 1:
            total_string += f"{relay_name} {relay_on_off} | "
    print(total_string,file=sys.stderr)
    print(total_string)

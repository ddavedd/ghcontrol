import time
import os
import subprocess
username = os.getlogin()

with open("/home/%s/ghcontrol/maps/%s_comp_read.map" % (username,username)) as f:
   connections = f.readlines()

if len(connections)>0:
   total_string = "Status: "
   for c in connections:
      x = c.strip().split(',')
      mread = x[4]
      if mread == "True":
         read_string = "mread"
         time.sleep(1)
      else:
         read_string = "read"
      print(x)
      print(read_string)
      if int(subprocess.check_output("%irelind %i %s %i" % (int(x[0]), int(x[1]), read_string, int(x[2])), shell=True)) == 1:
         total_string += x[3] + " " + x[5] + " | "
   print(total_string)


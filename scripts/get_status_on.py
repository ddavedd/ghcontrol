import os
import subprocess
username = os.getlogin()
with open("/home/%s/ghcontrol/%s_comp_read.map" % (username, username)) as f:
   lines = f.readlines()

on_names = "| ON: "
for l in lines:
   s = l.strip().split(",")
   command = "/usr/local/bin/%srelind" % s[0]
   x = subprocess.run([command, s[1], "read", s[2]],capture_output=True)
   if int(x.stdout) == 1:
      on_names += (s[3] + " ")
on_names += " |\n"
print(on_names)


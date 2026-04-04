import os
import subprocess

with open("hh1_comp_read.map") as f:
	connections = f.readlines()
	
if len(connections)>0:
	total_string = ""
	for c in connections:
		x = c.strip().split(',')
		if int(subprocess.check_output("%irelind %i read %i" % (int(x[0]),int(x[1]),int(x[2])), shell=True)) == 1:
			total_string += x[3] + " " + x[4] + " | "
	print(total_string)

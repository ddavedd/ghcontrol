import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime
import dateutil

with open('test.txt','r') as f:
   lines = f.readlines()

xvals = []
yvals = []
for l in lines:
   sl = l.split()
   if len(sl) ==3 :
      datetimeval = dateutil.parser.parse(sl[0] + " " + sl[1])
      xvals.append(datetimeval)
      yvals.append(float(sl[2]))

#print(xvals)
#print(yvals)
x = np.array(xvals)
y = np.array(yvals)
print(x)
print(y)

current_date_string = lines[0].split()[0]
fig, ax = plt.subplots()
ax.plot(x,y,label="Temperature")
# X axis
# Setting the datetime for start and end of day
x_low = x[0].replace(hour=0,minute=0,second=0)
x_high = x[0].replace(hour=23,minute=59,second=59)
ax.set_xlim(x_low,x_high)
xloc = md.HourLocator(interval=2)
major_format = md.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(major_format)
ax.xaxis.set_major_locator(xloc)
fig.autofmt_xdate()
# Y axis
ax.set_ylim(25,100)
# Labels and legend
ax.set_title("Temperature %s" % current_date_string)
ax.set_xlabel("Time")
ax.set_ylabel("Temperature Fahrenheit")
ax.legend()
# Save image
fig.savefig('%s.png' % current_date_string)

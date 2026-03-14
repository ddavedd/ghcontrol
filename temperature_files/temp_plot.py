import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib.patches import Rectangle
from matplotlib.ticker import MultipleLocator
import numpy as np
import datetime
import dateutil
import sys
import os

username = os.getlogin()
ALPHA = .4
BOX_HEIGHT = 5
HEATER_TEMP = 25
HEATER_COLOR = 'yellow'
EXHAUST_FAN_TEMP = 90
EXHAUST_FAN_COLOR = 'red'
TOP_FAN_TEMP = 95
TOP_FAN_COLOR = 'green'
HAF_FAN_TEMP = 30
HAF_FAN_COLOR = 'blue'

def draw_heater(axes, times, start_temp=HEATER_TEMP, end_temp=HEATER_TEMP+BOX_HEIGHT, color=HEATER_COLOR, alpha=ALPHA, label="Heater"):
   return draw_multiple_rects(axes,times,start_temp,end_temp,color,alpha,label)
   
def draw_exhaust_fan(axes, times, start_temp=EXHAUST_FAN_TEMP, end_temp=EXHAUST_FAN_TEMP+BOX_HEIGHT, color=EXHAUST_FAN_COLOR, alpha=ALPHA, label="Exhaust Fan"):
   return draw_multiple_rects(axes,times,start_temp,end_temp,color,alpha,label)

def draw_top_fan(axes, times, start_temp=TOP_FAN_TEMP, end_temp=TOP_FAN_TEMP+BOX_HEIGHT, color=TOP_FAN_COLOR, alpha=ALPHA, label="Top Fan"):
   return draw_multiple_rects(axes,times,start_temp,end_temp,color,alpha,label)
   
def draw_haf_fan(axes, times, start_temp=HAF_FAN_TEMP, end_temp=HAF_FAN_TEMP+BOX_HEIGHT, color=HAF_FAN_COLOR, alpha=ALPHA, label="HAF Fan"):
   return draw_multiple_rects(axes,times,start_temp,end_temp,color,alpha,label)

def draw_multiple_rects(axes, times, start_temp, end_temp, color, alpha,label):
   for t in range(0,len(times),2):
      if t+1 < len(times):
         r = draw_rect(axes,times[t],times[t+1],start_temp,end_temp,color, alpha,label)
   return r
   
def draw_rect(axes, start_time, end_time, start_temp, end_temp, color='purple', alpha=1.0, label="Unknown"):
   r = Rectangle((start_time, start_temp), end_time - start_time, end_temp - start_temp)
   r.set(color=color, alpha=alpha, label=label)
   axes.add_patch(r)
   return r

DPI_PNG = 100
if len(sys.argv)>2:
   DPI_PNG = int(sys.argv[2])

print(sys.argv[1])
with open(sys.argv[1],'r') as f:
   lines = f.readlines()
#sides = []
#with open(sys.argv[3],'r') as f:
#   sides = f.readlines()

xvals = []
# Make a matrix of the y values (temps) + at the end write the average
number_samples_plus_average = len(lines[0].split())-2+1
yvals = [[] for x in range(number_samples_plus_average)]
print(yvals)
for l in lines:
   sl = l.split()
   if len(sl) >= 3 :
      datetimeval = dateutil.parser.parse(sl[0] + " " + sl[1])
      xvals.append(datetimeval)
      average = 0.0
      for i in range(number_samples_plus_average - 1):
         value = float(sl[2+i])
         yvals[i].append(value)
         average += value
      average = average / (number_samples_plus_average - 1)
      yvals[-1].append(float("%.1f" % average))
print(yvals)

#MOVING_AVERAGE_SIZE = 500
#averages = yvals[-1]
#moving_average_list = []
#average_smooth = []
#for a in averages:
#   moving_average_list.append(a)
#   if len(moving_average_list)>MOVING_AVERAGE_SIZE:
#      moving_average_list = moving_average_list[1:]
#   smooth_value = sum(moving_average_list)/len(moving_average_list)
#   if len(moving_average_list) >= int(MOVING_AVERAGE_SIZE/2):
#      average_smooth.append(smooth_value)
#   #print(moving_average_list)
#for i in range(int(MOVING_AVERAGE_SIZE/2)-1):
#   average_smooth.append(smooth_value)
#yvals.append(average_smooth)
   
#sx = []
#sy = []
#for s in sides:
#   ss = s.split()
#   if len(ss) == 3:
##      datetimeval = dateutil.parser.parse(ss[0] + " " + ss[1])
#      sx.append(datetimeval)
#      sy.append(float(ss[2]))
      
#print(xvals)
#print(yvals)
#x = np.array(xvals)
#y = np.array(yvals)
#sx = np.array(sx)
#sy = np.array(sy)

#print(x)
#print(y)
#print(sx)
#print(sy)

current_date_string = lines[0].split()[0]
fig, ax = plt.subplots()
for i in range(len(yvals)):
   # For individual temperature sensors
   if i < len(yvals)-1:
      alpha = .25
      color = "gray"
      linewidth = 1
      label = None
   # For the average temperature
   else:
      alpha = 1.0
      color = "blue"
      linewidth = 1
      label = "Average Temp"
#   else:
#      alpha = .80
#      color = "green"
#      linewidth = 1
#      label="Smooth Average"
   ax.plot(xvals,yvals[i],label=label,alpha=alpha, color=color, linewidth=linewidth)
# ax.plot(xvals,yvals[0],label="Temperature")
# X axis
# Setting the datetime for start and end of day
x_low = xvals[0].replace(hour=0,minute=0,second=0)
x_high = x_low + datetime.timedelta(days=1)
ax.set_xlim(x_low,x_high)
xloc = md.HourLocator(interval=2)
xloc_minor = md.HourLocator(interval=1)
major_format = md.DateFormatter('%I %p')
ax.xaxis.set_major_formatter(major_format)
ax.xaxis.set_major_locator(xloc)
ax.xaxis.set_minor_locator(xloc_minor)
ax.tick_params(which="major",length=10)
ax.tick_params(which="minor",length=4)
fig.autofmt_xdate(rotation=45,ha='center')
ax.yaxis.set_major_locator(MultipleLocator(10))
ax.yaxis.set_minor_locator(MultipleLocator(5))
#ax2 = ax.twinx()
#ax2.set_ylim(0,100)
#ax2.plot(sx,sy,label="Rollup Sides % Open",color="green")
# Y axis
minimum = min([min(y) for y in yvals])
maximum = max([max(y) for y in yvals])
ax.set_ylim(minimum,maximum)
# Labels and legend
ax.grid(visible=True)
ax.set_title(username)
ax.set_xlabel(current_date_string)
ax.set_ylabel("Temperature Fahrenheit")
ax.legend()

times = []
for i in range(0,29):
   times.append(x_low + datetime.timedelta(hours=i))

rs = []
rs.append(draw_heater(ax,times))
rs.append(draw_exhaust_fan(ax,times[1:]))
rs.append(draw_haf_fan(ax,times[2:]))
rs.append(draw_top_fan(ax,times))
#ax.legend(handles=rs)
print([r.get_label() for r in rs])
# Save image
fig.savefig('/home/%s/ghcontrol/temperature_files/png/%s.png' % (username, current_date_string), dpi=DPI_PNG)


import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib.patches import Rectangle
import numpy as np
import datetime
import dateutil
import sys

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

DPI_PNG = 150
if len(sys.argv)>2:
   DPI_PNG = int(sys.argv[2])

print(sys.argv[1])
with open(sys.argv[1],'r') as f:
   lines = f.readlines()
sides = []
with open(sys.argv[3],'r') as f:
   sides = f.readlines()
xvals = []
yvals = []
for l in lines:
   sl = l.split()
   if len(sl) >= 3 :
      datetimeval = dateutil.parser.parse(sl[0] + " " + sl[1])
      xvals.append(datetimeval)
      yvals.append(float(sl[2]))


sx = []
sy = []
for s in sides:
   ss = s.split()
   if len(ss) == 3:
      datetimeval = dateutil.parser.parse(ss[0] + " " + ss[1])
      sx.append(datetimeval)
      sy.append(float(ss[2]))
      
#print(xvals)
#print(yvals)
x = np.array(xvals)
y = np.array(yvals)
sx = np.array(sx)
sy = np.array(sy)

print(x)
print(y)
print(sx)
print(sy)

current_date_string = lines[0].split()[0]
fig, ax = plt.subplots()
ax.plot(x,y,label="Temperature")
# X axis
# Setting the datetime for start and end of day
x_low = x[0].replace(hour=0,minute=0,second=0)
x_high = x[0].replace(hour=23,minute=59,second=59)
ax.set_xlim(x_low,x_high)
xloc = md.HourLocator(interval=3)
xloc_minor = md.HourLocator(interval=1)
major_format = md.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(major_format)
ax.xaxis.set_major_locator(xloc)
ax.xaxis.set_minor_locator(xloc_minor)
fig.autofmt_xdate()
ax2 = ax.twinx()
ax2.set_ylim(0,100)
ax2.plot(sx,sy,label="Rollup Sides % Open",color="green")
# Y axis
ax.set_ylim(25,100)
# Labels and legend
ax.grid(visible=True)
ax.set_title("Temperature %s" % current_date_string)
ax.set_xlabel("Time")
ax.set_ylabel("Temperature Fahrenheit")
ax.legend()

times = []
for i in range(0,29):
   times.append(x_low + datetime.timedelta(hours=i))

#draw_rect(ax,x_low, x_high,30,40,"red",.5)
#draw_rect(ax,x_low,x_high,35,45,"orange", .5)
rs = []
rs.append(draw_heater(ax,times))
rs.append(draw_exhaust_fan(ax,times[1:]))
rs.append(draw_haf_fan(ax,times[2:]))
rs.append(draw_top_fan(ax,times))
ax2.legend(handles=rs)
print([r.get_label() for r in rs])
# Save image
fig.savefig('png/%s.png' % current_date_string, dpi=DPI_PNG)

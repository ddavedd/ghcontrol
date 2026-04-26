"""The master control script for the temperature of the greenhouse"""
import os
import datetime
import time
USERNAME = os.getlogin()
control_values = []

def call_script(script_name):
    """Call script from scripts directory"""
    script_dir = f"/home/{USERNAME}/ghcontrol/scripts/"
    script_path = script_dir + script_name
    print(f"Control temp calling {script_name}")
    os.system(script_path)

try:
    with open(f"/home/{USERNAME}/ghcontrol/control_files/{USERNAME}.control", encoding="utf-8") as f:
        for line in f.readlines():
            control_values.append(line.strip().split())
except FileNotFoundError:
    print("No control values file found")

print(control_values)
controls = []
for c in control_values:
    if c[0] == "+":
        higher = True
    elif c[0] == "-":
        higher = False
    else:
        print(f"Unrecognized symbol for control temperatures {c[0]}")
        higher = False
    temp = float(c[1])
    diff = float(c[2])
    script_on = c[3]
    script_off = c[4]
    controls.append({'is_on': False, 'temp': temp, 'diff': diff, 'on_script': script_on, 'off_script': script_off, "higher": higher})

print(controls)
print("On reset, turn controls off automatically to return to original state")
for c in controls:
    call_script(c['off_script'])

# TODO check time to see if the temperatures are current (within last 60 secs?)
while True:
    try:
        with open(f"/home/{USERNAME}/ghcontrol/temperature_files/tempf/current.tempf", encoding="utf-8") as f:
            tempf_values = f.readlines()[0].strip().split()
    except FileNotFoundError:
        print("Error opening temperature file, not found")
    timestamp_day = tempf_values[0]
    timestamp_time = tempf_values[1]
    print(datetime.datetime.now())
    print(timestamp_day)
    print(timestamp_time)
    temps = tempf_values[2:]
    temps = [float(t) for t in temps]
    average_temp = sum(temps)/float(len(temps))
    temps_spread = max(temps) - min(temps)
    number_temps = len(temps)

    print(f"Average: {average_temp:.1}")
    print(f"Minimum: {min(temps):.1}")
    print(f"Maximum: {max(temps):.1}")
    print(f"Spread:  {temps_spread:.1}")
    print(f"Count:   {number_temps}")
    for c in controls:
        if not c["is_on"]:
            if c["higher"]:
                if average_temp > c["temp"]:
                    call_script(c['on_script'])
                    c["is_on"] = True
            else: # c["higher"] == False
                if average_temp < c["temp"]:
                    call_script(c['on_script'])
                    c["is_on"] = True
        else: # c["is_on"]
            if c["higher"]:
                if average_temp < (c["temp"] - c["diff"]):
                    call_script(c['off_script'])
                    c["is_on"] = False
            else: # c["higher"] == False
                if average_temp > (c["temp"] + c["diff"]):
                    call_script(c['off_script'])
                    c["is_on"] = False
    time.sleep(14)

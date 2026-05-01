"""The master control script for the temperature of the greenhouse"""
import os
import datetime
import time
ON_INTERVAL = 5 # Seconds
TIMEOUT_WARNING = 120 # Seconds
HIGH_TEMP_ALERT_THRESHOLD = 94.0
LOW_TEMP_ALERT_THRESHOLD = 38.0
RESEND_TIME = 3600 # Seconds = 1 hour
USERNAME = os.getlogin()
control_values = []
sent_alert = False
sent_time = None

def call_script(script_name):
    """Call script from scripts directory"""
    script_dir = f"/home/{USERNAME}/ghcontrol/scripts/"
    script_path = script_dir + script_name
    print(f"Control temp calling {script_name}")
    os.system(script_path)

def call_alert(alert_name):
    """Call script from scripts directory"""
    global sent_alert
    global sent_time
    if sent_alert == False:
        script_dir = f"/home/{USERNAME}/ghcontrol/alerts/"
        script_path = script_dir + alert_name
        print(f"Control temp calling {alert_name}")
        sent_time = datetime.datetime.now()
        sent_alert = True
        os.system(script_path)
    else:
        print(f"Already sent alert, waiting for ({RESEND_TIME} seconds) resend, {(datetime.datetime.now()-sent_time).seconds} elapsed")

# Read Control File to setup thermostat control functions
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
time.sleep(10)

# Main Loop
while True:
    if sent_alert:
        if (datetime.datetime.now() - sent_time).seconds > RESEND_TIME:
            sent_alert = False
    try:
        with open(f"/home/{USERNAME}/ghcontrol/temperature_files/tempf/current.tempf", encoding="utf-8") as f:
            tempf_values = f.readlines()[0].strip().split()
    except FileNotFoundError:
        print("Error opening temperature file, not found")
        call_alert("no_temperature_file_found.sh")
    # Get the timestamp and values from file
    timestamp_day = tempf_values[0]
    timestamp_time = tempf_values[1]
    temps = tempf_values[2:]

    # Need to send alert if the temperature values is old, and we aren't getting new ones'
    current_time = datetime.datetime.now()
    last_temp_read = datetime.datetime.strptime(f"{timestamp_day} {timestamp_time}","%Y-%m-%d %H:%M:%S")
    print(f"Current time is {current_time}")
    print(f"Last temperature read was {last_temp_read}")
    time_diff_seconds = (current_time - last_temp_read).seconds
    print(f"Difference in seconds: {time_diff_seconds}")
    if time_diff_seconds > TIMEOUT_WARNING:
        call_alert("control_timeout_msmtp_mail.sh")
    temps = [float(t) for t in temps]
    average_temp = sum(temps)/float(len(temps))
    temps_spread = max(temps) - min(temps)
    number_temps = len(temps)
    if average_temp > HIGH_TEMP_ALERT_THRESHOLD:
        call_alert("high_temp_msmtp_mail.sh")
    if average_temp < LOW_TEMP_ALERT_THRESHOLD:
        call_alert("low_temp_msmtp_mail.sh")

    print(f"Average: {average_temp:.1f}")
    print(f"Minimum: {min(temps):.1f}")
    print(f"Maximum: {max(temps):.1f}")
    print(f"Spread:  {temps_spread:.1f}")
    print(f"Count:   {number_temps}")
    for c in controls:
        if not c["is_on"]:
            if c["higher"]:
                if average_temp > c["temp"]:
                    call_script(c['on_script'])
                    c["is_on"] = True
                    time.sleep(ON_INTERVAL)
            else: # c["higher"] == False
                if average_temp < c["temp"]:
                    call_script(c['on_script'])
                    c["is_on"] = True
                    time.sleep(ON_INTERVAL)
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

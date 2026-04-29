import datetime
import time

names = ["Heater_North_Tstat"]
x = open("2026-04-26.tomatogh.log")

BTUS_PER_GAL_PROPANE = 91500
BTU_HEATER = 200000
DOLLAR_PER_GALLON = 2.03
EXHAUST_FAN_AMPS = 6.0
HAF_FAN_AMPS = 4.0
NAME = 0
ON_OFF = 1
TIMESTAMP_DATE = 2
TIMESTAMP_TIME = 3
TIMESTAMP_TIMEZONE = 4
FORMAT = "%Y-%m-%d %H:%M:%S"
total_seconds = 0
current_on = None


lines = x.readlines()
for l in lines:
    split_line = l.strip().split(" ")
    if split_line[NAME] == names[0]:
        if split_line[ON_OFF] == "On":
            current_on = datetime.datetime.strptime(f"{split_line[TIMESTAMP_DATE]} {split_line[TIMESTAMP_TIME]}", FORMAT)
        elif split_line[ON_OFF] == "Off":
            if current_on:
                time_d = datetime.datetime.strptime(f"{split_line[TIMESTAMP_DATE]} {split_line[TIMESTAMP_TIME]}", FORMAT) - current_on
                total_seconds += time_d.total_seconds()
                current_on is None

hours = total_seconds / (3600.0)
gallons = (hours*BTU_HEATER)/BTUS_PER_GAL_PROPANE
dollars = gallons*DOLLAR_PER_GALLON
print(f"Total hours on for {names[0]}: {hours}")
print(f"Total gallons: {gallons}")
print(f'Total cost: {dollars}')

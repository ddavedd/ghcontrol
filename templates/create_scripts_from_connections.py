import os
ROLLUP_TIME_MINUTE = 3
RELAY_DESCRIPTION = 0
RELAY_VALUE = 1
RELAY_VALUE_REVERSER = 2
SCRIPT_LINE = "#! /usr/bin/bash\n"

DEBOUNCE_TIME_MS = 200  # 200 milliseconds

def create_menu_entry(username, menu_name):
    menu_entry = "[Desktop Entry]\nName=%s\nComment=\nIcon=folder\nType=Directory\n"
    menu_filename = "/home/%s/.local/share/desktop-directories/%s.directory" % (username, menu_name)
    write_file(menu_filename, menu_entry)

def create_menus(username, names):
   create_menu_entry(username, "Greenhouse")
   for name in names:
      create_menu_entry(username, name)

def get_filename(event_description, relay_description):
   return "%s_%s" % (event_description, relay_description)

def log_event(username, event_description, relay_description):
   return "/home/%s/ghcontrol/scripts/log_event.sh \"%s %s\"\n" % (username, event_description, relay_description)

def activate_relay(board_type, board_number, relay_number, relay_value):
   return "/usr/local/bin/%irelind %i write %i %i\n" % (int(board_type), int(board_number), int(relay_number), int(relay_value))

def create_desktop_launcher(username, script_dir, event_description, relay_description):
   launcher_text = "[Desktop Entry]\nName=%s_%s\n" % (event_description, relay_description)
   launcher_text += "Exec=/home/%s/ghcontrol/scripts/%s.sh\n" % (username, get_filename(event_description, relay_description))
   launcher_text += "Comment=\nTerminal=true\nIcon=gnome-panel-launcher\nType=Application\n"
   launcher_file_name = "/home/%s/.local/share/applications/%s_%s" % (username, event_description, relay_description)
   write_file(launcher_file_name, launcher_text, ".desktop")

def write_file(file_name, file_text, file_ending=".sh"):
   print(file_name + file_ending)
   with open(file_name+file_ending, 'w') as f:
      f.write(file_text)		
   print(file_text)

def add_to_category(cat_dict, category_name, file_name, file_ending=".sh"):
   if category_name not in cat_dict:
      cat_dict[category_name] = []
   cat_dict[category_name].append(file_name)
   return cat_dict

def create_xml_menu(cat_dict):
   #import xml.etree.ElementTree as ET
   total_menu = ""
   for k,v in cat_dict:
      menu_text = "<Menu>\n"
      menu_text += "\t<Name>%s</Name>\n" % k
      menu_text += "\t<Directory>%s.directory</Directory>\n" % k
      for v_i in sorted(v):
         menu_text += "\t<Include><Filename>%s.desktop</Filename></Include>\n" % v_i
      menu_text += "\t<Layout>\n\t\t<Merge type=\"menus\"/>\n"
      for v_i in sorted(v):
         menu_text += "\t\t<Filename>%s.desktop</Filename>\n" % v_i
      menu_text += "\t\t<Merge type=\"files\"/>\n"
      menu_text += "\t</Layout>\n</Menu>\n"
      total_menu += menu_text
   return total_menu

def create_directory_entries(username, cat_dict):
   directory_entry_location = "/home/%s/.local/share/desktop-directories/" % username
   for k,v in cat_dict:
      directory_text = "[Desktop Entry]\nName=%s\nComment=\nIcon=folder\nType=Directory\n" % k
      write_file(directory_entry_location + k, directory_text,".directory")

username = os.getlogin()
buttons_setup_text = ""
buttons_function_text = "import os\n"
buttons_function_text += "import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library\n"
buttons_function_text += "GPIO.setwarnings(False)\n"
buttons_function_text += "GPIO.setmode(GPIO.BOARD)\n\n"

relay_map = {"8": [], "3": [], "PI_PINS": [], "ARDUINO_PINS": [],}
menu_cats = {}
scripts_dir = "/home/%s/ghcontrol/scripts/" % username
categories = []
with open("/home/%s/ghcontrol/connection_files_actual/%s.connections" % (username,username)) as connections:
   lines = connections.readlines()
   
for l in lines:
   line_dict = {}
   print(l)
   items = l.split()
   for i in items:
      split_item = i.split('=')
      line_dict[split_item[0]] = split_item[1]
   print(line_dict)
   match line_dict['type']:
      case "ON_OFF_SINGLE":
         relay_map[line_dict['relay_board_type']].append([line_dict['relay1'], line_dict['name']])
         relay_type = [["On",1],["Off",0]]
         for r in relay_type:
            relay1 = line_dict['relay1'].split(',')
            file_name = get_filename(line_dict['name'], r[RELAY_DESCRIPTION])
            file_text = SCRIPT_LINE
            file_text += log_event(username, line_dict['name'], r[RELAY_DESCRIPTION])
            file_text += activate_relay(line_dict['relay_board_type'], relay1[0], relay1[1], r[RELAY_VALUE]) 
            write_file(scripts_dir + file_name, file_text)
            create_desktop_launcher(username, scripts_dir, line_dict['name'], r[RELAY_DESCRIPTION])
            menu_cats = add_to_category(menu_cats, line_dict['category'], file_name)
      case "ON_OFF_DOUBLE":
         relay_map[line_dict['relay_board_type']].append([line_dict['relay1'], line_dict['name']])
         relay_map[line_dict['relay_board_type']].append([line_dict['relay2'], line_dict['name']])
         relay_type = [["On",1],["Off",0]]
         for r in relay_type:
            relay1 = line_dict['relay1'].split(',')
            relay2 = line_dict['relay2'].split(',')
            file_name = get_filename(line_dict['name'], r[RELAY_DESCRIPTION])
            file_text = SCRIPT_LINE
            file_text += log_event(username, line_dict['name'], r[RELAY_DESCRIPTION])
            file_text += activate_relay(line_dict['relay_board_type'], relay1[0], relay1[1], r[RELAY_VALUE])
            file_text += activate_relay(line_dict['relay_board_type'], relay2[0], relay2[1], r[RELAY_VALUE])
            write_file(scripts_dir + file_name, file_text)
            create_desktop_launcher(username, scripts_dir, line_dict['name'], r[RELAY_DESCRIPTION])
            menu_cats = add_to_category(menu_cats, line_dict['category'], file_name)
      case "REVERSING_PAIR":
         relay_type = [["Up",1,0],["Down",0,1],["Stop",0,0]]
         relay_map[line_dict['relay_board_type']].append([line_dict['relay1'], line_dict['name']])
         relay_map[line_dict['relay_board_type']].append([line_dict['relay2'], line_dict['name']])
         for r in relay_type:
            relay1 = line_dict['relay1'].split(',')
            relay2 = line_dict['relay2'].split(',')
            file_name = get_filename(line_dict['name'], r[RELAY_DESCRIPTION])
            file_text = SCRIPT_LINE
            file_text += log_event(username, line_dict['name'], r[RELAY_DESCRIPTION])
            file_text += activate_relay(line_dict['relay_board_type'], relay1[0], relay1[1], r[RELAY_VALUE])
            file_text += activate_relay(line_dict['relay_board_type'], relay2[0], relay2[1], r[RELAY_VALUE_REVERSER])
            write_file(scripts_dir + file_name, file_text)
            create_desktop_launcher(username, scripts_dir, line_dict['name'], r[RELAY_DESCRIPTION])
            menu_cats = add_to_category(menu_cats, line_dict['category'], file_name)
      case "PUSH_BUTTON":
         name = line_dict['name']
         up_pin, down_pin, stop_pin = line_dict["up_pin"], line_dict["down_pin"], line_dict["stop_pin"]
         relay_map["PI_PINS"].append([up_pin,name + "_UP"])
         relay_map["PI_PINS"].append([down_pin,name + "_DOWN"])
         relay_map["PI_PINS"].append([stop_pin,name + "_STOP"])
         
         buttons = [["Up", up_pin],["Down",down_pin],["Stop",stop_pin]]
         stop_name = buttons[2][0]
         for b in buttons:
            pin_number = b[1]
            up_down_stop = b[0]
            buttons_function_text += "def button_callback_%s(channel):\n" % pin_number
            buttons_function_text += "\tprint(\"%s button pressed, %s %s\")\n" % (pin_number, line_dict['name'], up_down_stop)
            buttons_function_text += "\tos.system(\"%s.sh\")\n" % (scripts_dir + line_dict['name'] + "_" +  up_down_stop)
            buttons_function_text += "\tos.system(\"/usr/bin/sleep %im && %s.sh\")\n\n" % (ROLLUP_TIME_MINUTE, scripts_dir + line_dict['name'] + "_" + stop_name)
            buttons_setup_text += "GPIO.setup(%s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)\n" % pin_number
            buttons_setup_text += "GPIO.add_event_detect(%s,GPIO.RISING,callback=button_callback_%s, bouncetime=%i)\n\n" % (pin_number, pin_number, DEBOUNCE_TIME_MS)
      case "PRESSURE_SENSOR":
         relay_map["ARDUINO_PINS"].append([line_dict['analog_pin'],line_dict['name']])
         print("Pressure Sensor not yet implemented")
      case "FLOW_METER":
         relay_map["ARDUINO_PINS"].append([line_dict['digital_pin'],line_dict['name']])
         print("Flow Meter not yet implemented")
      #file_name = get_filename(line_dict['name'], "Pushed")
      #file_text = SCRIPT_LINE
      #file_text += log_event(username, line_dict['name'], "Pushed")
      #write_file(scripts_dir + file_name, file_text)
      case _:
         print("RELAY TYPE NOT SUPPORTED: %s" % c[EVENT_TYPE])
end_text = "message = input(\"Press Enter to Quit\\n\")\n"
end_text += "GPIO.cleanup()\n"
write_file("/home/%s/ghcontrol/on_reset/buttons_setup" % username, buttons_function_text + buttons_setup_text + end_text, ".py")

create_directory_entries(username, menu_cats.items())
subcats = create_xml_menu(sorted(menu_cats.items()))
create_directory_entries(username, {"Greenhouse": []}.items())
total_menu_xml = open("/home/%s/ghcontrol/templates/raspi_menu_start.xml" % username).read() + subcats + open("/home/%s/ghcontrol/templates/raspi_menu_end.xml" % username).read()
write_file("/home/%s/.config/menus/rpd-applications" % username, total_menu_xml,".menu")

def write_map_category(map_category, description):
   map_text = "-----------------------------------\n"
   map_text += description + "\n"
   for m in sorted(map_category):
      map_text += str(m) + "\n"
   return map_text

def write_map_category_comp(cat_description, map_category):
   map_text = ""
   for s in sorted(map_category):
      map_text += "%s,%s,%s\n" % (cat_description[0], s[0],s[1])
   return map_text
      
      
comp_map_text = write_map_category_comp(["8"], relay_map["8"])
comp_map_text += write_map_category_comp(["3"], relay_map["3"])
total_map_text = write_map_category(relay_map["8"], "8 Relay Board")
total_map_text += write_map_category(relay_map["3"], "3 Relay Board")
total_map_text += write_map_category(relay_map["PI_PINS"], "Raspberry Pi GPIO Pins")
total_map_text += write_map_category(relay_map["ARDUINO_PINS"], "Arduino Pins")
print(total_map_text)
write_file("/home/%s/ghcontrol/%s_connections" % (username, username), total_map_text, ".map")
write_file("/home/%s/ghcontrol/%s_comp_read" % (username, username), comp_map_text, ".map")

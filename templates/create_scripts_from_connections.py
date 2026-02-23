import os
EVENT_DESCRIPTION = 0
EVENT_CATEGORY = 1
BOARD_TYPE = 2
BOARD_NUMBER = 3
RELAY_NUMBER = 4
EVENT_TYPE = 5
DOUBLE_BOARD_TYPE = 6
DOUBLE_BOARD_NUMBER = 7
DOUBLE_RELAY_NUMBER = 8

BUTTON_NUMBER = 3
BUTTON_PULL_UP_DOWN = 4

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

connections = open("connections.txt")
menu_cats = {}
for c in connections:
   scripts_dir = "/home/%s/ghcontrol/scripts/" % username
   categories = []
   c = c.split()
   print(c)
   if c[EVENT_TYPE] == "ON_OFF_SINGLE":
      relay_type = [["On",1],["Off",0]]
      for r in relay_type:
         file_name = get_filename(c[EVENT_DESCRIPTION], r[RELAY_DESCRIPTION])
         file_text = SCRIPT_LINE
         file_text += log_event(username, c[EVENT_DESCRIPTION], r[RELAY_DESCRIPTION])
         file_text += activate_relay(c[BOARD_TYPE
         ], c[BOARD_NUMBER], c[RELAY_NUMBER], r[RELAY_VALUE]) 
         write_file(scripts_dir + file_name, file_text)
         create_desktop_launcher(username, scripts_dir, c[EVENT_DESCRIPTION], r[RELAY_DESCRIPTION])
         menu_cats = add_to_category(menu_cats, c[EVENT_CATEGORY], file_name)
   elif c[EVENT_TYPE] == "ON_OFF_DOUBLE":
      relay_type = [["On",1],["Off",0]]
      for r in relay_type:
         file_name = get_filename(c[EVENT_DESCRIPTION], r[RELAY_DESCRIPTION])
         file_text = SCRIPT_LINE
         file_text += log_event(username, c[EVENT_DESCRIPTION], r[RELAY_DESCRIPTION])
         file_text += activate_relay(c[BOARD_TYPE], c[BOARD_NUMBER], c[RELAY_NUMBER], r[RELAY_VALUE])
         file_text += activate_relay(c[DOUBLE_BOARD_TYPE], c[DOUBLE_BOARD_NUMBER], c[DOUBLE_RELAY_NUMBER], r[RELAY_VALUE])
         write_file(scripts_dir + file_name, file_text)
         create_desktop_launcher(username, scripts_dir, c[EVENT_DESCRIPTION], r[RELAY_DESCRIPTION])
         menu_cats = add_to_category(menu_cats, c[EVENT_CATEGORY], file_name)
   elif c[EVENT_TYPE] == "REVERSING_PAIR":
      relay_type = [["Up",1,0],["Down",0,1],["Off",0,0]]
      for r in relay_type:
         file_name = get_filename(c[EVENT_DESCRIPTION], r[RELAY_DESCRIPTION])
         file_text = SCRIPT_LINE
         file_text += log_event(username, c[EVENT_DESCRIPTION], r[RELAY_DESCRIPTION])
         file_text += activate_relay(c[BOARD_TYPE], c[BOARD_NUMBER], c[RELAY_NUMBER], r[RELAY_VALUE])
         file_text += activate_relay(c[DOUBLE_BOARD_TYPE], c[DOUBLE_BOARD_NUMBER], c[DOUBLE_RELAY_NUMBER], r[RELAY_VALUE_REVERSER])
         write_file(scripts_dir + file_name, file_text)
         create_desktop_launcher(username, scripts_dir, c[EVENT_DESCRIPTION], r[RELAY_DESCRIPTION])
         menu_cats = add_to_category(menu_cats, c[EVENT_CATEGORY], file_name)
   elif c[EVENT_TYPE] == "PUSH_BUTTON":
      buttons_function_text += "def %s_button_callback(channel):\n" % c[BUTTON_NUMBER]
      buttons_function_text += "\tprint(\"%s button pressed\")\n" % c[BUTTON_NUMBER]
      buttons_function_text += "\tos.system(\"%s.sh\")\n\n" % (scripts_dir + c[EVENT_DESCRIPTION])
      buttons_setup_text += "GPIO.setup(%s, GPIO.IN, pull_up_down=GPIO.%s)\n" % (c[BUTTON_NUMBER], c[BUTTON_PULL_UP_DOWN])
      buttons_setup_text += "GPIO.add_event_detect(%s,GPIO.RISING,callback=%s_button_callback, bouncetime=%i)\n\n" % (c[BUTTON_NUMBER], c[BUTTON_NUMBER], DEBOUNCE_TIME_MS)
       
      #file_name = get_filename(c[EVENT_DESCRIPTION], "Pushed")
      #file_text = SCRIPT_LINE
      #file_text += log_event(username, c[EVENT_DESCRIPTION], "Pushed")
      #write_file(scripts_dir + file_name, file_text)
   else:
         print("RELAY TYPE NOT SUPPORTED: %s" % c[EVENT_TYPE])
end_text = "message = input(\"Press Enter to Quit\\n\")\n"
end_text += "GPIO.cleanup()\n"
write_file("/home/%s/ghcontrol/on_reset/buttons_setup" % username, buttons_function_text + buttons_setup_text + end_text, ".py")

create_directory_entries(username, menu_cats.items())
subcats = create_xml_menu(sorted(menu_cats.items()))
create_directory_entries(username, {"Greenhouse": []}.items())
total_menu_xml = open("raspi_menu_start.xml").read() + subcats + open("raspi_menu_end.xml").read()
write_file("/home/%s/.config/menus/rpd-applications" % username, total_menu_xml,".menu")


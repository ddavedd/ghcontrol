"""Create scripts from connections file"""
import os
ROLLUP_TIME_MINUTE = 3
RELAY_DESCRIPTION = 0
RELAY_VALUE = 1
RELAY_VALUE_REVERSER = 2
SCRIPT_LINE = "#! /usr/bin/bash\n"

DEBOUNCE_TIME_MS = 200  # 200 milliseconds

def create_menu_entry(username, menu_name):
    """Create Menu Entry for raspberry pi start menu"""
    menu_entry = "[Desktop Entry]\nName=%s\nComment=\nIcon=folder\nType=Directory\n"
    menu_filename = f"/home/{username}/.local/share/desktop-directories/{menu_name}.directory"
    write_file(menu_filename, menu_entry)

def create_menus(username, names):
    """Create full menu"""
    create_menu_entry(username, "Greenhouse")
    for menu_name in names:
        create_menu_entry(username, menu_name)

def get_filename(event_description, relay_description):
    """Make filename out of event + relay description"""
    return f"{event_description}_{relay_description}"

def log_event(username, event_description, relay_description):
    """Log the event"""
    return f"/home/{username}/ghcontrol/scripts/log_event.sh \"{event_description} {relay_description}\"\n"

def activate_relay(board_type, board_number, relay_number, relay_value, relay_is_485=False):
    """Activate relay 8relind or 3relind"""
    if relay_is_485:
        return f"/usr/local/bin/{board_type}relind {board_number} mwrite {relay_number} {relay_value}\n/usr/bin/sleep .5s\n"
    return f"/usr/local/bin/{board_type}relind {board_number} write {relay_number} {relay_value}\n"

def create_desktop_launcher(username, script_dir, event_description, relay_description):
    """Create launcher for menu entries"""
    launcher_text = f"[Desktop Entry]\nName={event_description}_{relay_description}\n"
    launcher_text += f"Exec=/home/{username}/ghcontrol/scripts/{get_filename(event_description, relay_description)}.sh\n"
    launcher_text += "Comment=\nTerminal=true\nIcon=gnome-panel-launcher\nType=Application\n"
    launcher_file_name = f"/home/{username}/.local/share/applications/{event_description}_{relay_description}"
    write_file(launcher_file_name, launcher_text, ".desktop")

def write_file(writefile_name, writefile_text, file_ending=".sh"):
    """Write a file to computer"""
    print(writefile_name + file_ending)
    with open(writefile_name+file_ending, 'w', encoding="utf-8") as f:
        f.write(writefile_text)
    print(writefile_text)

def add_to_category(cat_dict, category_name, category_file_name, file_ending=".sh"):
    """Add to a category"""
    if category_name not in cat_dict:
        cat_dict[category_name] = []
    cat_dict[category_name].append(category_file_name)
    return cat_dict

def create_xml_menu(cat_dict):
    """Create the xml menu for raspberry pi start menu"""
    #import xml.etree.ElementTree as ET
    total_menu = ""
    for key,val in cat_dict:
        menu_text = "\t\t<Menu>\n"
        menu_text += f"\t\t<Name>{key}</Name>\n"
        menu_text += f"\t\t<Directory>{key}.directory</Directory>\n"
        for v_i in sorted(val):
            menu_text += f"\t\t<Include><Filename>{v_i}.desktop</Filename></Include>\n"
        menu_text += "\t\t<Layout>\n\t\t\t<Merge type=\"menus\"/>\n"
        for v_i in sorted(val):
            menu_text += f"\t\t\t<Filename>{v_i}.desktop</Filename>\n"
        menu_text += "\t\t\t<Merge type=\"files\"/>\n"
        menu_text += "\t\t</Layout>\n\t\t</Menu>\n"
        total_menu += menu_text
    return total_menu

def create_directory_entries(username, cat_dict):
    """Create the desktop entries for the menu"""
    directory_entry_location = f"/home/{username}/.local/share/desktop-directories/"
    for key,val in cat_dict:
        directory_text = "[Desktop Entry]\nName={key}\nComment=\nIcon=folder\nType=Directory\n"
        write_file(directory_entry_location + key, directory_text,".directory")

USER = os.getlogin()
buttons_setup_text = ""
buttons_function_text = "import os\n"
buttons_function_text += "from gpiozero import Button\n"
buttons_function_text += "from signal import pause\n\n"
relay_map = {"8": [], "3": [], "PI_PINS": [], "ARDUINO_PINS": [],}
menu_cats = {}
scripts_dir = f"/home/{USER}/ghcontrol/scripts/"
categories = []

with open(f"/home/{USER}/ghcontrol/connection_files_actual/{USER}.connections", encoding="utf-8") as connections:
    lines = connections.readlines()

for l in lines:
    line_dict = {}
    print(l)
    items = l.split()
    for i in items:
        split_item = i.split('=')
        line_dict[split_item[0]] = split_item[1]
    print(line_dict)
    is_485 = bool('is_485' in line_dict) #.keys())
    #if 'is_485' in line_dict.keys():
    #    is_485 = True
    #else:
    #    is_485 = False
    match line_dict['type']:
        case "ON_OFF_SINGLE":
            if "normally_closed" in line_dict: #.keys():
                relay_type = [["On",0],["Off",1]]
                relay_map[line_dict['relay_board_type']].append([line_dict['relay1'], line_dict['name'], is_485, "OFF"])
            else:
                relay_type = [["On",1],["Off",0]]
                relay_map[line_dict['relay_board_type']].append([line_dict['relay1'], line_dict['name'], is_485, "ON"])
            for r in relay_type:
                relay1 = line_dict['relay1'].split(',')
                file_name = get_filename(line_dict['name'], r[RELAY_DESCRIPTION])
                file_text = SCRIPT_LINE
                file_text += log_event(USER, line_dict['name'], r[RELAY_DESCRIPTION])
                file_text += activate_relay(line_dict['relay_board_type'], relay1[0], relay1[1], r[RELAY_VALUE], is_485)
                write_file(scripts_dir + file_name, file_text)
                create_desktop_launcher(USER, scripts_dir, line_dict['name'], r[RELAY_DESCRIPTION])
                menu_cats = add_to_category(menu_cats, line_dict['category'], file_name)
        case "ON_OFF_DOUBLE":
            relay_map[line_dict['relay_board_type']].append([line_dict['relay1'], line_dict['name'], is_485, "ON"])
            relay_map[line_dict['relay_board_type']].append([line_dict['relay2'], line_dict['name'], is_485, "ON"])
            relay_type = [["On",1],["Off",0]]
            for r in relay_type:
                relay1 = line_dict['relay1'].split(',')
                relay2 = line_dict['relay2'].split(',')
                file_name = get_filename(line_dict['name'], r[RELAY_DESCRIPTION])
                file_text = SCRIPT_LINE
                file_text += log_event(USER, line_dict['name'], r[RELAY_DESCRIPTION])
                file_text += activate_relay(line_dict['relay_board_type'], relay1[0], relay1[1], r[RELAY_VALUE], is_485)
                file_text += activate_relay(line_dict['relay_board_type'], relay2[0], relay2[1], r[RELAY_VALUE], is_485)
                write_file(scripts_dir + file_name, file_text)
                create_desktop_launcher(USER, scripts_dir, line_dict['name'], r[RELAY_DESCRIPTION])
                menu_cats = add_to_category(menu_cats, line_dict['category'], file_name)
        case "REVERSING_PAIR": ###
            if 'name_style' in line_dict: #.keys():
                if line_dict['name_style'] == "updownstop":
                    relay_type = [["Up",1,0],["Down",0,1],["Stop",0,0]]
                elif line_dict['name_style'] == "openclosestop":
                    relay_type = [["Open",1,0],["Close",0,1],["Stop",0,0]]
                else:
                    relay_type = [["FirstRelayOn",1,0],["SecondRelayOn",0,1],["BothRelaysOff",0,0]]
            else:
                relay_type = [["FirstRelayOn",1,0],["SecondRelayOn",0,1],["BothRelaysOff",0,0]]
            relay_map[line_dict['relay_board_type']].append([line_dict['relay1'], line_dict['name'], is_485, relay_type[0][0]])
            relay_map[line_dict['relay_board_type']].append([line_dict['relay2'], line_dict['name'], is_485, relay_type[1][0]])
            for r in relay_type:
                relay1 = line_dict['relay1'].split(',')
                relay2 = line_dict['relay2'].split(',')
                file_name = get_filename(line_dict['name'], r[RELAY_DESCRIPTION])
                file_text = SCRIPT_LINE
                file_text += log_event(USER, line_dict['name'], r[RELAY_DESCRIPTION])
                file_text += activate_relay(line_dict['relay_board_type'], relay1[0], relay1[1], r[RELAY_VALUE], is_485)
                file_text += activate_relay(line_dict['relay_board_type'], relay2[0], relay2[1], r[RELAY_VALUE_REVERSER], is_485)
                write_file(scripts_dir + file_name, file_text)
                create_desktop_launcher(USER, scripts_dir, line_dict['name'], r[RELAY_DESCRIPTION])
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
                buttons_function_text += f"def button_callback_{pin_number}():\n"
                buttons_function_text += f"\tos.system(\"{scripts_dir + "log_event.sh"} '{pin_number} Button Pressed, {line_dict['name']} {up_down_stop}'\")\n"
                buttons_function_text += f"\tos.system(\"{scripts_dir + line_dict['name'] + "_" +  up_down_stop}.sh\")\n\n"
                buttons_setup_text += f"button_{pin_number} = Button(pin={pin_number}, pull_up=False,hold_time=.5)\n"
                buttons_setup_text += f"button_{pin_number}.when_held = button_callback_{pin_number}\n\n"
        case "PRESSURE_SENSOR":
            relay_map["ARDUINO_PINS"].append([line_dict['analog_pin'],line_dict['name']])
            print("Pressure Sensor not yet implemented")
        case "FLOW_METER":
            relay_map["ARDUINO_PINS"].append([line_dict['digital_pin'],line_dict['name']])
            print("Flow Meter not yet implemented")
        #file_name = get_filename(line_dict['name'], "Pushed")
        #file_text = SCRIPT_LINE
        #file_text += log_event(USER, line_dict['name'], "Pushed")
        #write_file(scripts_dir + file_name, file_text)
        case _:
            print(f"RELAY TYPE NOT SUPPORTED: {line_dict['type']}")
END_TEXT = "pause()\n"#"message = input(\"Press Enter to Quit\\n\")\n"
write_file(f"/home/{USER}/ghcontrol/on_reset/buttons_setup", buttons_function_text + buttons_setup_text + END_TEXT, ".py")

create_directory_entries(USER, menu_cats.items())
subcats = create_xml_menu(sorted(menu_cats.items()))
create_directory_entries(USER, {"Greenhouse": []}.items())
START_MENU_XML = open(f"/home/{USER}/ghcontrol/templates/raspi_menu_start.xml", encoding="utf-8").read()
END_MENU_XML = open(f"/home/{USER}/ghcontrol/templates/raspi_menu_end.xml", encoding="utf-8").read()
total_menu_xml = START_MENU_XML + subcats + END_MENU_XML
write_file(f"/home/{USER}/.config/menus/rpd-applications", total_menu_xml, ".menu")

def write_map_category(map_category, description):
    """Write the human readable map for connections"""
    map_text = "-----------------------------------\n"
    map_text += description + "\n"
    for m in sorted(map_category):
        map_text += str(m) + "\n"
    return map_text

def write_map_category_comp(cat_description, map_category):
    """Write the computer readable map for connections"""
    map_text = ""
    for s in sorted(map_category):
        map_text += f"{cat_description[0]},{s[0]},{s[1]},{s[2]},{s[3]}\n"
    return map_text

comp_map_text = write_map_category_comp(["8"], relay_map["8"])
comp_map_text += write_map_category_comp(["3"], relay_map["3"])
total_map_text = write_map_category(relay_map["8"], "8 Relay Board")
total_map_text += write_map_category(relay_map["3"], "3 Relay Board")
total_map_text += write_map_category(relay_map["PI_PINS"], "Raspberry Pi GPIO Pins")
total_map_text += write_map_category(relay_map["ARDUINO_PINS"], "Arduino Pins")
print(total_map_text)
write_file(f"/home/{USER}/ghcontrol/maps/{USER}_connections", total_map_text, ".map")
write_file(f"/home/{USER}/ghcontrol/maps/{USER}_comp_read", comp_map_text, ".map")

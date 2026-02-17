EVENT_DESCRIPTION = 0
BOARD_TYPE = 1
BOARD_NUMBER = 2
RELAY_NUMBER = 3
EVENT_TYPE = 4
DOUBLE_BOARD_TYPE = 5
DOUBLE_BOARD_NUMBER = 6
DOUBLE_RELAY_NUMBER = 7

RELAY_DESCRIPTION = 0
RELAY_VALUE = 1
RELAY_VALUE_REVERSER = 2
SCRIPT_LINE = "!/usr/bin/bash\n"
   
connections = open("connections.txt")
for c in connections:
   c = c.split()
   print(c)
   if c[EVENT_TYPE] == "ON_OFF_SINGLE":
      relay_type = [["On",1],["Off",0]]
      for r in relay_type:
         file_name = "%s_%s.sh" % (c[EVENT_DESCRIPTION],r[RELAY_DESCRIPTION])
         file_text = SCRIPT_LINE
         file_text += "/home/USERNAME/ghcontrol/log_event.sh \"" + c[EVENT_DESCRIPTION] + " " + r[RELAY_DESCRIPTION] + "\"\n"
         file_text += "/usr/local/bin/%irelind %i write %i %i\n" % (int(c[BOARD_TYPE]),int(c[BOARD_NUMBER]),int(c[RELAY_NUMBER]), int(r[RELAY_VALUE])) 
         print(file_name)
         print(file_text)
   elif c[EVENT_TYPE] == "ON_OFF_DOUBLE":
      relay_type = [["On",1],["Off",0]]
      for r in relay_type:
         file_name = "%s_%s.sh" % (c[EVENT_DESCRIPTION],r[RELAY_DESCRIPTION])
         file_text = SCRIPT_LINE
         file_text += "/home/USERNAME/ghcontrol/log_event.sh \"" + c[EVENT_DESCRIPTION] + " " + r[RELAY_DESCRIPTION] + "\"\n"
         for x in [[c[BOARD_TYPE],c[BOARD_NUMBER],c[RELAY_NUMBER]],[c[DOUBLE_BOARD_TYPE],c[DOUBLE_BOARD_NUMBER],c[DOUBLE_RELAY_NUMBER]]]:
            file_text += "/usr/local/bin/%irelind %i write %i %i\n" % (int(x[0]),int(x[1]),int(x[2]), int(r[RELAY_VALUE]))
         print(file_name)
         print(file_text)
   elif c[EVENT_TYPE] == "REVERSING_PAIR":
      relay_type = [["Up",1,0],["Down",0,1],["Off",0,0]]
      for r in relay_type:
         file_name = "%s_%s.sh" % (c[EVENT_DESCRIPTION],r[RELAY_DESCRIPTION])
         file_text = SCRIPT_LINE
         file_text += "/home/USERNAME/ghcontrol/log_event.sh \"" + c[EVENT_DESCRIPTION] + " " + r[RELAY_DESCRIPTION] + "\"\n"
         file_text += "/usr/local/bin/%irelind %i write %i %i\n" % (int(c[BOARD_TYPE]),int(c[BOARD_NUMBER]),int(c[RELAY_NUMBER]), int(r[RELAY_VALUE]))
         file_text += "/usr/local/bin/%irelind %i write %i %i\n" % (int(c[DOUBLE_BOARD_TYPE]),int(c[DOUBLE_BOARD_NUMBER]),int(c[DOUBLE_RELAY_NUMBER]),int(r[RELAY_VALUE_REVERSER]))
         print(file_name)
         print(file_text)
   else:
      print("RELAY TYPE NOT SUPPORTED: %s" % c[EVENT_TYPE])

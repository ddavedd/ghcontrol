import os
user = os.getlogin()
graphs_directory = "/home/%s/ghcontrol/temperature_files/png/" % user
logs_directory = "/home/%s/ghcontrol/logs/" % user
print("Creating index")
print("Graphs directory "+graphs_directory)
print("Logs directory "+logs_directory)
files_list = []
for f in os.listdir(graphs_directory):
   if f.endswith(".png"):
      files_list.append([f,"./graphs/"+f])
   
for f in os.listdir(logs_directory):
   if f.endswith(".log"):
      files_list.append([f,"./reports/"+f])

html = "<html>\n<body>\n<ul>\n"

files_list.sort(reverse=True)
for f in files_list:
   html += "<li><a href='%s'>%s</a></li>\n" % (f[1],f[0])
html += "</ul>\n</body>\n</html>\n"
with open("index.html","w") as f:
   f.write(html)


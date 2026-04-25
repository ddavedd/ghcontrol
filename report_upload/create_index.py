""" Create an index file for our reports and graphs to be uploaded
"""
import os
username = os.getlogin()
print("Report Upload")
print("User is " + str(username))
graphs_directory = f"/home/{username}/ghcontrol/temperature_files/png/"
logs_directory = f"/home/{username}/ghcontrol/logs/"
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
    html += f"<li><a href='{f[1]}'>{f[0]}</a></li>\n"
html += "</ul>\n</body>\n</html>\n"
with open("index.html","w",encoding="utf-8") as f:
    f.write(html)

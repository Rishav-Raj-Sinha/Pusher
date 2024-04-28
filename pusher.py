import tkinter as tk
from tkinter import ttk
import subprocess
import os
from crontab import CronTab
from datetime import datetime

def collecting_values():
    global user_path 
    global user_time 
    user_path = path.get()
    user_time = time.get()
    global integer_user_time
    integer_user_time = int(user_time)
    
def script_maker():
    script_template = """
    #!/bin/bash

    cd "{}"
    git add .
    git commit -m "Scheduled push"
    git push
    """.format(user_path)
    print(script_template)
    script_filename = "pusher.sh"
    with open(script_filename, "w") as file:
        file.write(script_template)
    global path 
    path = os.path.abspath(script_filename)
    subprocess.run(["chmod", "+x", script_filename])
#    subprocess.run(["./" + script_filename],shell=True)

def scheduler():
    cron = CronTab(user=True)
    command = path
    job = cron.new(command=command, comment='scheduled push')
    current_time = datetime.now()
    desired_time = current_time.replace(hour=integer_user_time, second=0, microsecond=0)
    job.minute.on(desired_time.minute+1)
    job.hour.on(desired_time.hour)
    job.day.on(desired_time.day)
    job.month.on(desired_time.month)
    job.dow.on(desired_time.weekday())
    cron.write()

def function_caller():
    collecting_values()
    script_maker()
    scheduler()

main  = tk.Tk()
main.title('Pusher')

#dimensions of the tkinter window1
window_width = 400
window_height = 200
main.resizable(0, 0)

#padding for the window
main['padx'] = 20
main['pady'] = 5

# get the screen dimension
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
main.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

#grid layout
main.columnconfigure(0, weight=1)
main.columnconfigure(1, weight=5)

#theming
main.configure(bg='black')

#creating the path entry and time entry widget
path = tk.StringVar()
time = tk.StringVar()

path_label = ttk.Label(main,text="Enter the path to your project directory",foreground="white",background="black")
#path_label.pack(anchor=tk.W,padx=10,pady=5,fill='x', expand=True)
path_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=20)
path_box = ttk.Entry(main, textvariable=path)
#path_box.pack(anchor=tk.W,padx=10,pady=5,fill=tk.X)
path_box.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=20)

time_label = ttk.Label(main,text="Enter the time for push",foreground="white",background="black")
#time_label.pack(anchor=tk.W,padx=10,pady=5,fill='x', expand=True)
time_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=20)

time_box = ttk.Entry(main, textvariable=time)
#time_box.pack(anchor=tk.W,padx=10,pady=5,fill=tk.X)
time_box.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=20)

login_button = ttk.Button(main, text="Schedule",command=function_caller)
login_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=20)


main.mainloop()


import sqlite3
#import library to switch between files
from subprocess import call
import subprocess
#import os to access directories
import os
#import gui libraries
import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
from tkinter import font
#import sys for closing window and terminating script fully, when user closes window
import sys
#import libraries for data graphs to be created and placed on window
#matplotlib documentation was used for finding graphs and for learning how the code works for each graph: https://matplotlib.org/stable/
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 

#class for changing fonts of labels
class Font(ctk.CTkFont):
    def __init__(self, family, size, weight):
        super().__init__(family=family, size=size, weight=weight)

#classes to create widgets
class Entry(ctk.CTkEntry):
    def __init__(self, master, show, textvariable, **kwargs):             
        super().__init__(master, show=show , textvariable=textvariable)
        self.place(**kwargs)

class Label(ctk.CTkLabel):
    def __init__(self, master, text,font=None, **kwargs):
        super().__init__(master, text=text, font=font)
        self.place(**kwargs)

class Button(ctk.CTkButton):
    def __init__(self, master, text, command, **kwargs):
        super().__init__(master, text=text, command=command)
        self.place(**kwargs)

#class to create window
class window(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        #set title, window size and make it so the user cannot change the size 
        self.title("FitPro")
        self.geometry("900x500")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.close_everything)

        #create fonts
        self.title_font = Font(family="Helvetica", size = 20,weight="bold")
        self.colour_key_font = Font(family="Helvetica", size = 10,weight="bold")
        #create and place widgets
        self.title_label = Label(self, "Data visualisation (some extra graphs)",font = self.title_font, x=270, y=10)
        self.colour_key = Label(self, "Blue = True\nRed = False",font = self.colour_key_font, x=650, y=50)
        self.goback_button = Button(self, "Go back\nto plan", self.go_back,x=10,y=10)
        #call method automatically when window runs
        self.get_info()


    def get_info(self):
        #get information
        with open("Scripts/user_plan_key.txt","r") as f:
                plan_key = f.readline()
        conn = sqlite3.connect("information.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_personal_info WHERE id=?", (plan_key))
        personal_info = cur.fetchone()
        cur.execute("SELECT * FROM equipment_access WHERE id=?", (plan_key))
        equipment_access = cur.fetchone()
        conn.close()
        
         #get information from user_personal_info table
        self.current_weight = personal_info[3]
        self.weight_goal = personal_info[4]
        self.physical_activity = personal_info[5]
        self.workout_type = personal_info[6]
        self.gym_access = personal_info[7]
        #get information from eqipment_access table
        self.dumbells = equipment_access[3]
        self.pull_up_bar = equipment_access[4]
        self.barbell = equipment_access[5]
        self.bench = equipment_access[6]
        self.leg_extensions_machine = equipment_access[7]
        self.leg_curl_machine = equipment_access[8]
        self.ez_bar = equipment_access[9]
        self.cables = equipment_access[10]
        self.dip_station = equipment_access[11]
        self.leg_press_machine = equipment_access[12]
        self.pec_fly_machine = equipment_access[13]
        self.skipping_rope = equipment_access[14]
        self.tricep_press_machine = equipment_access[15]
        self.treadmill = equipment_access[16]
        self.stair_climber_machine = equipment_access[17]
        self.exercise_bike = equipment_access[18]
        self.shoulder_press_machine = equipment_access[19]
        self.chest_press_machine = equipment_access[20]
        self.rowing_machine = equipment_access[21]
        self.preacher_curl_bench = equipment_access[22]
        self.lateral_pulldown_machine = equipment_access[23]
        #call method
        self.display_weight_graph()

    #method will display graphs to show information about the user's plan
    def display_weight_graph(self):
        #create labels
        labels = ["current weight","weight goal"]
        #get values
        values = [self.current_weight,self.weight_goal]
        #set size of graph, set x and y axis values, set title
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.bar(labels, values)
        ax.set_ylabel('weight (KG)')
        ax.set_title('Weight goal')
        #convert to tkinter format and place graph
        canvas = FigureCanvasTkAgg(fig, master=self)
        weight_graph = canvas.get_tk_widget()
        weight_graph.place(x=100,y=150) 
        #call next graph method
        self.display_equipment_access_graph()

    def display_equipment_access_graph(self):
        #create labels
        labels = ['Dumbells', 'Pull Up Bar', 'Barbell', 'Bench', 'Leg Extension', 'Leg Curl', 'EZ Bar', 'Cables',
                'Dip Station', 'Leg Press', 'Pec Fly', 'Skipping Rope', 'Tricep Press', 'Treadmill', 'Stair Climber',
                'Exercise Bike', 'Shoulder Press', 'Chest Press', 'Rowing Machine', 'Preacher Curl Bench', 'Lateral Pulldown\nMachine']
        #get values
        values = [self.dumbells, self.pull_up_bar, self.barbell, self.bench, self.leg_extensions_machine,
                    self.leg_curl_machine, self.ez_bar, self.cables, self.dip_station, self.leg_press_machine,
                    self.pec_fly_machine, self.skipping_rope, self.tricep_press_machine, self.treadmill, self.stair_climber_machine,
                    self.exercise_bike, self.shoulder_press_machine, self.chest_press_machine, self.rowing_machine,
                    self.preacher_curl_bench, self.lateral_pulldown_machine]
        #create true or false colours
        colours = ['#ff9999', '#66b3ff']
        #create list for labels of segments
        segments = []
        #create list for segment colours
        segment_colours = []

        #iterate through labels and values lists, 
        #and set the colour of each segment
        for i in range(len(labels)):
            label = labels[i]
            value = values[i]
            if value == 1:
                colour_index = 1
            else:
                colour_index = 0
            segments.append(label)
            segment_colours.append(colours[colour_index])
        #set graph size
        fig, ax = plt.subplots(figsize=(6, 5))
        #make sure every segment is equal size (first parameter)
        ax.pie([1]*len(segments), labels=segments, colors=segment_colours, startangle=180)
        #set title
        ax.set_title('Equipment access')
        #convert to tkinter format and place graph
        canvas = FigureCanvasTkAgg(fig, master=self)
        equipment_access_graph = canvas.get_tk_widget()
        equipment_access_graph.place(x=700, y=150)

    #go back to plan
    def go_back(self):
        script_path = os.path.join("Scripts", "display_plan.py")
        subprocess.run(["python", script_path])
        self.close_everything()

    def close_everything(self):
        children = self.winfo_children()
        for widget in children:
            widget.destroy()
        self.quit()
        #sys used to terminate script fully
        sys.exit() 

#run window
if __name__ == "__main__":
    app = window()
    app.mainloop()

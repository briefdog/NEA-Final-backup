#This file will take information from workout_details and display it
#User cannot run this window unless they go through the process of creating a plan, 
#or they have created a plan and they have accessed it through manage_fitness_plans.py

#import GUI
import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
from tkinter import font
import os
#import sqlite3 to access database and to run queries
import sqlite3

#import library to switch between files
import subprocess
from subprocess import call

#class to change font of labels
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

        self.title("FitPro")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.manage_fitness_plans_button = Button(self, "Manage fitness\nplans", self.manage_fitness_plans, x=10, y=10)
        self.homepage_button = Button(self, "Return to\nhomepage", self.homepage, x=10, y=49)

        self.title_font = Font("Helvetica", 30, None)
        self.day_font = Font("Helvetica", 30, "bold")
        self.exercise_font = Font("Helvetica", 20, "bold")
        self.instructions_font = Font("Helvetica", 20, None)
        
        self.title_label = Label(self,"This is your workout plan:",self.title_font,x=350,y=5)
        self.instructions_label = Label(self,"You can use this workout split, and adjust it to your own schedule.\nIt is recommended to have a rest day between each cycle,\nor at least one rest day each week to prevent injury.\nMake sure to listen to your body and take additional\nrest days if overly sore or fatigued.",self.instructions_font,x=230,y=410)
        self.pushday_label = Label(self,"Push day",self.day_font,x=200,y=50)
        self.pushday_label = Label(self,"Pull day",self.day_font,x=450,y=50)
        self.pushday_label = Label(self,"Legs day",self.day_font,x=700,y=50)
        self.push_ex_1 = Label(self,"",self.exercise_font,x=200,y=100)
        self.push_ex_2 = Label(self,"",self.exercise_font,x=200,y=150)
        self.push_ex_3 = Label(self,"",self.exercise_font,x=200,y=200)
        self.push_ex_4 = Label(self,"",self.exercise_font,x=200,y=250)
        self.push_ex_5 = Label(self,"",self.exercise_font,x=200,y=300)
        self.push_ex_6 = Label(self,"",self.exercise_font,x=200,y=350)
        self.pull_ex_1 = Label(self,"",self.exercise_font,x=450,y=100)
        self.pull_ex_2 = Label(self,"",self.exercise_font,x=450,y=150)
        self.pull_ex_3 = Label(self,"",self.exercise_font,x=450,y=200)
        self.pull_ex_4 = Label(self,"",self.exercise_font,x=450,y=250)
        self.pull_ex_5 = Label(self,"",self.exercise_font,x=450,y=300)
        self.pull_ex_6 = Label(self,"",self.exercise_font,x=450,y=350)
        self.legs_ex_1 = Label(self,"",self.exercise_font,x=700,y=100)
        self.legs_ex_2 = Label(self,"",self.exercise_font,x=700,y=150)
        self.legs_ex_3 = Label(self,"",self.exercise_font,x=700,y=200)
        self.legs_ex_4 = Label(self,"",self.exercise_font,x=700,y=250)
        self.legs_ex_5 = Label(self,"",self.exercise_font,x=700,y=300)
        self.legs_ex_6 = Label(self,"",self.exercise_font,x=700,y=350)
        #call method when window runs
        self.collect_info()

    #method will collect plan key and select the record corresponding to the plan key, from workout_plan_details
    def collect_info(self):
        with open("Scripts/user_plan_key.txt","r") as f:
                plan_key = f.readline()
        conn = sqlite3.connect("information.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM workout_plan_details WHERE id=?", (plan_key))
        self.workout_plan = cur.fetchone()
        #call method
        self.update_widgets()

    #method will collect information from workout_plan_details and change the texts of the labels
    def update_widgets(self):
        #collect exercises
        push_exercise_1 = self.workout_plan[3]
        push_exercise_2 = self.workout_plan[4]
        push_exercise_3 = self.workout_plan[5]
        push_exercise_4 = self.workout_plan[6]
        push_exercise_5 = self.workout_plan[7]
        push_exercise_6 = self.workout_plan[8]
        pull_exercise_1 = self.workout_plan[9]
        pull_exercise_2 = self.workout_plan[10]
        pull_exercise_3 = self.workout_plan[11]
        pull_exercise_4 = self.workout_plan[12]
        pull_exercise_5 = self.workout_plan[13]
        pull_exercise_6 = self.workout_plan[14]
        legs_exercise_1 = self.workout_plan[15]
        legs_exercise_2 = self.workout_plan[16]
        legs_exercise_3 = self.workout_plan[17]
        legs_exercise_4 = self.workout_plan[18]
        legs_exercise_5 = self.workout_plan[19]
        legs_exercise_6 = self.workout_plan[20]
        
        #change texts for first four exercises
        self.push_ex_1.configure(text=f"1. {push_exercise_1}")
        self.push_ex_2.configure(text=f"2. {push_exercise_2}")
        self.push_ex_3.configure(text=f"3. {push_exercise_3}")
        self.push_ex_4.configure(text=f"4. {push_exercise_4}")

        self.pull_ex_1.configure(text=f"1. {pull_exercise_1}")
        self.pull_ex_2.configure(text=f"2. {pull_exercise_2}")
        self.pull_ex_3.configure(text=f"3. {pull_exercise_3}")
        self.pull_ex_4.configure(text=f"4. {pull_exercise_4}")

        self.legs_ex_1.configure(text=f"1. {legs_exercise_1}")
        self.legs_ex_2.configure(text=f"2. {legs_exercise_2}")
        self.legs_ex_3.configure(text=f"3. {legs_exercise_3}")
        self.legs_ex_4.configure(text=f"4. {legs_exercise_4}")

        self.push_ex_1.configure(text=f"1. {push_exercise_1}")
        self.push_ex_2.configure(text=f"2. {push_exercise_2}")
        self.push_ex_3.configure(text=f"3. {push_exercise_3}")
        self.push_ex_4.configure(text=f"4. {push_exercise_4}")

        self.pull_ex_1.configure(text=f"1. {pull_exercise_1}")
        self.pull_ex_2.configure(text=f"2. {pull_exercise_2}")
        self.pull_ex_3.configure(text=f"3. {pull_exercise_3}")
        self.pull_ex_4.configure(text=f"4. {pull_exercise_4}")

        self.legs_ex_1.configure(text=f"1. {legs_exercise_1}")
        self.legs_ex_2.configure(text=f"2. {legs_exercise_2}")
        self.legs_ex_3.configure(text=f"3. {legs_exercise_3}")
        self.legs_ex_4.configure(text=f"4. {legs_exercise_4}")

        #if statements are used to prevent the texts from getting changed to "None"
        if push_exercise_5 is not None:

            self.push_ex_5.configure(text=f"5. {push_exercise_5}")
            self.pull_ex_5.configure(text=f"5. {pull_exercise_5}")
            self.legs_ex_5.configure(text=f"5. {legs_exercise_5}")

        if push_exercise_6 is not None:

            self.push_ex_6.configure(text=f"6. {push_exercise_6}")
            self.pull_ex_6.configure(text=f"6. {pull_exercise_6}")
            self.legs_ex_6.configure(text=f"6. {legs_exercise_6}")

    #method to go to manage_fitness_plans page
    def manage_fitness_plans(self):
        script_path = os.path.join("Scripts", "manage_fitness_plans.py")
        subprocess.run(["python", script_path])
        self.close_everything()

    def homepage(self):
        script_path = os.path.join("Scripts", "homepage.py")
        subprocess.run(["python", script_path])
        self.close_everything()

    #method to delete every widget before closing window
    def close_everything(self):
        children = self.winfo_children()
        for widget in children:
            widget.destroy()
        self.quit()
        
#run window
if __name__ == "__main__":
    app = window()
    app.mainloop()

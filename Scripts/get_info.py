import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
from tkinter import font
import os
import sqlite3

import subprocess
from subprocess import call

#class for changing fonts of labels
class CheckBox(ctk.CTkCheckBox):
    def __init__(self, master, text,variable,onvalue,offvalue,**kwargs):
        super().__init__(master, text=text,variable=variable,onvalue=onvalue,offvalue=offvalue)
        self.place(**kwargs)

class Font(ctk.CTkFont):
    def __init__(self, family, size, weight):
        super().__init__(family=family, size=size, weight=weight)

class ComboBox(ctk.CTkComboBox):
    def __init__(self,master,values, **kwargs):
        super().__init__(master,values=values)
        self.place(**kwargs)

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

class window(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FitPro")
        self.geometry("720x710")
        self.resizable(False, False)
        
        self.title_font = Font("Helvetica", 30, "bold")
        self.question_font = Font("Helvetica", 18,"bold")
        self.explanation_font = Font("Helvetica",18,"bold")

        #store values of entry boxes from q1 and q2
        self.q1 = StringVar()
        self.q2 = StringVar()

        #store checkbox values as boolean variables
        self.dumbells_box = BooleanVar(value=False)
        self.pullupbar_box = BooleanVar(value=False)
        self.barbell_box = BooleanVar(value=False)
        self.bench_box = BooleanVar(value=False)
        self.legextension_box = BooleanVar(value=False)
        self.legcurl_box = BooleanVar(value=False)
        self.ezbar_box = BooleanVar(value=False)
        self.cables_box = BooleanVar(value=False)
        self.dipstation_box = BooleanVar(value=False)
        self.legpress_box = BooleanVar(value=False)
        self.pecfly_box = BooleanVar(value=False)
        self.skippingrope_box = BooleanVar(value=False)
        self.triceppress_box = BooleanVar(value=False)
        self.treadmill_box = BooleanVar(value=False)
        self.stairclimber_box = BooleanVar(value=False)
        self.exercisebike_box = BooleanVar(value=False)
        self.shoulderpress_box = BooleanVar(value=False)
        self.chestpress_box = BooleanVar(value=False)
        self.rowingmachine_box = BooleanVar(value=False)
        self.preachercurl_bench_box = BooleanVar(value=False)
        self.lateralpulldown_machine_box = BooleanVar(value=False)
        self.monday_box = BooleanVar(value=False)
        self.tuesday_box = BooleanVar(value=False)
        self.wednesday_box = BooleanVar(value=False)
        self.thursday_box = BooleanVar(value=False)
        self.friday_box = BooleanVar(value=False)
        self.saturday_box = BooleanVar(value=False)
        self.sunday_box = BooleanVar(value=False)

        #create widgets
        self.createfitnessplan_label = Label(self,"Create your own fitness plan",font=self.title_font,x=180,y=10)
        self.goback_button = Button(self,"Return to homepage", self.goback,x=10,y=15)
        self.heading = Label(self,"Answer these questions and we will create a plan for you:",font = self.explanation_font,x=10,y=60)
        self.question1 = Label(self,"1. What is your current weight? (KG)",font=self.question_font,x=10,y=90)
        self.question2 = Label(self,"2. What is your weight goal? (KG)",font=self.question_font,x=10,y=160)
        self.question3 = Label(self,"3. How much physical activity do you usually do in a week?",font=self.question_font,x=10,y=230)
        self.question4 = Label(self,"4. Do you have any allergies?",font=self.question_font,x=10,y=300)
        self.question5 = Label(self,"5. Do you have access to the gym?",font=self.question_font,x=10,y=360)
        self.question6 = Label(self,"(If answer to question 5 was yes) \n6. Tick the boxes of the equipment that you have access to:",font=self.question_font,x=10,y=500)
        self.submit_button = Button(self,"Submit",self.get_info,x=250,y=665)
        self.q1_entry = Entry(self,"",self.q1,x=50,y=120)
        self.q2_entry = Entry(self,"",self.q2,x=50,y=190)
        self.q3_combobox = ComboBox(self,values = ["low","moderate","vigorous"],x=50,y=260)
        self.q4_combobox = ComboBox(self,values = ["yes","no","I don't know"],x=50,y=330)
        self.q5_combobox = ComboBox(self,values = ["yes","no"],x=50,y=390)
        #create checkboxes for equipment access
        self.dumbells_checkbox = CheckBox(self, "Dumbells", self.dumbells_box, True,False,x=10,y=545)
        self.pullupbar_checkbox = CheckBox(self, "Pull up bar", self.pullupbar_box, True,False,x=120,y=545)
        self.barbell_checkbox = CheckBox(self, "Barbell", self.barbell_box, True,False,x=215,y=545)
        self.bench_checkbox = CheckBox(self, "Bench", self.bench_box, True,False,x=350,y=545)
        self.legextension_checkbox = CheckBox(self, "Leg extension\nmachine", self.legextension_box, True,False,x=460,y=540)
        self.legcurl_checkbox = CheckBox(self, "Leg curl\nmachine", self.legcurl_box, True,False,x=580,y=540)
        self.ezbar_checkbox = CheckBox(self, "EZ bar", self.ezbar_box, True,False,x=120,y=575)
        self.cables_checkbox = CheckBox(self, "Cables", self.cables_box, True,False,x=465,y=575)
        self.dipstation_checkbox = CheckBox(self, "Dip\nstation", self.dipstation_box, True,False,x=352,y=575)
        self.legpress_checkbox = CheckBox(self, "Leg press\n machine", self.legpress_box, True,False,x=10,y=575)
        self.pecfly_checkbox = CheckBox(self, "Pec fly\nmachine", self.pecfly_box, True,False,x=580,y=575)
        self.skippingrope_checkbox = CheckBox(self, "Skipping rope", self.skippingrope_box, True,False,x=215,y=575)
        self.triceppress_checkbox = CheckBox(self, "Tricep press\nmachine", self.triceppress_box, True,False,x=10,y=610)
        self.treadmill_checkbox = CheckBox(self, "Treadmill", self.treadmill_box, True,False,x=120,y=610)
        self.stairclimber_checkbox = CheckBox(self, "Stair climber\nmachine", self.stairclimber_box, True,False,x=352,y=610)
        self.exercisebike_checkbox = CheckBox(self, "Exercise bike", self.exercisebike_box, True,False,x=465,y=610)
        self.shoulderpress_checkbox = CheckBox(self, "Shoulder press\nmachine", self.shoulderpress_box, True,False,x=215,y=610)
        self.chestpress_checkbox = CheckBox(self, "Chest press", self.chestpress_box, True,False,x=580,y=610)
        self.rowingmachine_checkbox = CheckBox(self, "Rowing machine", self.rowingmachine_box, True,False,x=10,y=645)
        self.preachercurl_bench_checkbox = CheckBox(self, "Preacher curl\nbench", self.preachercurl_bench_box, True,False,x=465,y=645)
        self.lateralpulldown_machine_checkbox = CheckBox(self, "Lateral pulldown\nmachine", self.lateralpulldown_machine_box, True,False,x=580,y=645)
        self.select_all_equipment_button = Button(self,"Select all\nequipment", self.select_all_equipment,x=250,y=435)

            
    def select_all_equipment(self):
        #check if all equipment checkboxes are already checked
        if (self.dumbells_box.get() and self.pullupbar_box.get() and self.barbell_box.get() and
            self.bench_box.get() and self.legextension_box.get() and self.legcurl_box.get() and
            self.ezbar_box.get() and self.cables_box.get() and self.dipstation_box.get() and
            self.legpress_box.get() and self.pecfly_box.get() and self.skippingrope_box.get() and
            self.triceppress_box.get() and self.treadmill_box.get() and self.stairclimber_box.get() and
            self.exercisebike_box.get() and self.shoulderpress_box.get() and self.chestpress_box.get() and
            self.rowingmachine_box.get() and self.preachercurl_bench_box.get() and
            self.lateralpulldown_machine_box.get()) == False:

            #Select all boxes
            self.dumbells_box.set(True)
            self.pullupbar_box.set(True)
            self.barbell_box.set(True)
            self.bench_box.set(True)
            self.legextension_box.set(True)
            self.legcurl_box.set(True)
            self.ezbar_box.set(True)
            self.cables_box.set(True)
            self.dipstation_box.set(True)
            self.legpress_box.set(True)
            self.pecfly_box.set(True)
            self.skippingrope_box.set(True)
            self.triceppress_box.set(True)
            self.treadmill_box.set(True)
            self.stairclimber_box.set(True)
            self.exercisebike_box.set(True)
            self.shoulderpress_box.set(True)
            self.chestpress_box.set(True)
            self.rowingmachine_box.set(True)
            self.preachercurl_bench_box.set(True)
            self.lateralpulldown_machine_box.set(True)
        else:
            #if not all values are ticked, then they will all get deselected
            equipment_values = [self.dumbells_box, self.pullupbar_box, self.barbell_box,
                        self.bench_box, self.legextension_box, self.legcurl_box,
                        self.ezbar_box, self.cables_box, self.dipstation_box,
                        self.legpress_box, self.pecfly_box, self.skippingrope_box,
                        self.triceppress_box, self.treadmill_box, self.stairclimber_box,
                        self.exercisebike_box, self.shoulderpress_box, self.chestpress_box,
                        self.rowingmachine_box, self.preachercurl_bench_box,
                        self.lateralpulldown_machine_box]
            
            for equipment in equipment_values:
                equipment.set(False)
        
    def goback(self):    
        script_path = os.path.join("Scripts", "homepage.py")
        subprocess.run(["python", script_path])
        self.close_everything()

    #method will collect all information from user and store as variable
    def get_info(self):
        #collect user primary key
        with open("Scripts/user_account_key.txt","r") as f:
                line = f.readline()
                parts = line.split(',') 
                self.number = parts[0].strip('(')
        #This will check if the user has reached the maximum number of plans
        conn = sqlite3.connect("information.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_personal_info WHERE user_fk = ?", (self.number,))
        rows = cur.fetchall()
        number_of_plans = len(rows)
        if number_of_plans < 3:

            self.current_weight = self.q1.get()
            self.weight_goal = self.q2.get()
            self.q3 = self.q3_combobox.get()
            self.q4 = self.q4_combobox.get()
            self.q5 = self.q5_combobox.get()
            self.dumbells = self.dumbells_box.get()
            self.pull_up_bar = self.pullupbar_box.get()
            self.barbell = self.barbell_box.get()
            self.bench = self.bench_box.get() 
            self.leg_extension = self.legextension_box.get()
            self.leg_curl = self.legcurl_box.get() 
            self.ez_bar = self.ezbar_box.get()
            self.cables = self.cables_box.get()
            self.dip_station = self.dipstation_box.get()
            self.leg_press = self.legpress_box.get()
            self.pec_fly = self.pecfly_box.get()
            self.skipping_rope = self.skippingrope_box.get()
            self.triceppress = self.triceppress_box.get()
            self.treadmill = self.treadmill_box.get()
            self.stairclimber = self.stairclimber_box.get()
            self.exercisebike = self.exercisebike_box.get()
            self.shoulderpress = self.shoulderpress_box.get()
            self.chestpress = self.chestpress_box.get()
            self.rowingmachine = self.rowingmachine_box.get()
            self.preachercurl_bench = self.preachercurl_bench_box.get()
            self.lateralpulldown_machine = self.lateralpulldown_machine_box.get()
        
            if (self.current_weight != "") and (self.weight_goal != ""):
                try:
                    self.current_weight = float(self.current_weight)
                    self.weight_goal = float(self.weight_goal)
                    #go to insert information
                    self.insert_info()
                except ValueError:
                    messagebox.showerror(title="Error", message="Questions 1 and 2 must be numbers")
                    self.q1_entry.delete(0,END)
                    self.q2_entry.delete(0,END)

            else:
                messagebox.showerror(title="Error", message="Weight or height cannot be empty")
                self.q1_entry.delete(0,END)
                self.q2_entry.delete(0,END)
            
        else:
            messagebox.showerror(title="Error",message = "There is only a maximum of 3 fitness plans that can be created")

    #method will insert information into the tables
    def insert_info(self):
        if os.path.isfile("information.db"):
            conn = sqlite3.connect("information.db")
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO user_personal_info (user_fk,current_weight,weight_goal,physical_activity,allergies,gym_access) VALUES (?,?,?,?,?,?)",
                        (self.number,self.current_weight,self.weight_goal,self.q3,self.q4,self.q5))

            conn.commit()
            conn.close()

            #if there is no gym access, it will use exercises that do not require any gym equipment
            if self.q5 == "yes":
                conn = sqlite3.connect("information.db")
                cur = conn.cursor()
                cur.execute(
                "INSERT INTO equipment_access (user_fk,dumbells,pull_up_bar,barbell,bench,leg_extensions_machine,leg_curl_machine,ez_bar,cables,dip_station,leg_press_machine,pec_fly_machine,skipping_rope,tricep_press_machine,treadmill,stair_climber_machine,exercise_bike,shoulder_press_machine,chest_press_machine,rowing_machine,preacher_curl_bench,lateral_pulldown_machine) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (self.number,self.dumbells,self.pull_up_bar,self.barbell,self.bench,self.leg_extension,self.leg_curl,self.ez_bar,self.cables,self.dip_station,self.leg_press,self.pec_fly,self.skipping_rope,self.triceppress,self.treadmill,self.stairclimber,self.exercisebike,self.shoulderpress,self.chestpress,self.rowingmachine,self.preachercurl_bench,self.lateralpulldown_machine))
                conn.commit()  
                conn.close()
            else:
                conn = sqlite3.connect("information.db")
                cur = conn.cursor()
                cur.execute(
                "INSERT INTO equipment_access (user_fk,dumbells,pull_up_bar,barbell,bench,leg_extensions_machine,leg_curl_machine,ez_bar,cables,dip_station,leg_press_machine,pec_fly_machine,skipping_rope,tricep_press_machine,treadmill,stair_climber_machine,exercise_bike,shoulder_press_machine,chest_press_machine,rowing_machine,preacher_curl_bench,lateral_pulldown_machine) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (self.number,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False))
                conn.commit()  
                conn.close()
            script_path = os.path.join("Scripts", "create_fitness_plan.py")
            subprocess.run(["python", script_path])
            self.close_everything()
        else:
            messagebox.showerror(title = "Error",message="Database does not exist")
            self.q1_entry.delete(0,END)
            self.q2_entry.delete(0,END)

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


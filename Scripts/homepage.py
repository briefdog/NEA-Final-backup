#import libraries
import subprocess
from subprocess import call
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import os
#import sys for closing window and terminating script fully, when user closes window
import sys
#import libraries for BMI graph to be created and placed on window
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 

#class for changing fonts of labels
class Font(ctk.CTkFont):
    def __init__(self, family, size, weight):
        super().__init__(family=family, size=size, weight=weight)

#classes to create widgets
class Switch(ctk.CTkSwitch):
    def __init__(self,master,text,**kwargs):
        super().__init__(master,text=text)
        self.place(**kwargs)

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

#class to create window
class window(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        #set title, window size and make it so the user cannot change the size 
        self.title("FitPro")
        self.geometry("950x700")
        self.resizable(False, False)

        #use variables to retrieve values from entries
        self.weight = StringVar()
        self.height = StringVar()
        self.cm = StringVar()
        self.mm = StringVar()

        #method called when user wants to close the window, so script gets fully terminated,
        #incase the user presses the close window button in the top right corner,
        #and the graph has already been created and placed at least once
        #(More explanation at the close_everything method)
        self.protocol("WM_DELETE_WINDOW", self.close_everything)

        #create font
        self.title_font = Font("Helvetica", 40, "bold")
        self.header_font = Font("Helvetica", 18,"bold" )
        self.bmi_label_font = Font("Helvetica", 22,"bold" )
        self.convertfrom_cm_font = Font("Helvetica", 12 ,"bold")
        self.ethnicityexplanation_font = Font("Helvetica", 15 ,"bold")

        #create and place widgets
        self.return_button = Button(self, "Log out", self.logout, x=20, y=20)
        self.homepage_label = Label(self, "Homepage", x=420, y=20, font=self.title_font)
        self.createplan_button = Button(self, "Create fitness plan?", self.create_plan, x=20, y=50)
        self.bmi_label = Label(self, "Calculate your BMI here:", x=350, y=430, font=self.bmi_label_font)
        self.weight_entry = Entry(self, "", self.weight, x=430, y=510)
        self.height_entry = Entry(self, "", self.height, x=430, y=470)
        self.weight_label = Label(self, "Weight:", x=350,y=510, font=self.header_font)
        self.height_label = Label(self, "Height", x=350, y=470, font=self.header_font)
        self.calculate_button = Button(self, "Calculate", self.calculate_bmi, x=430, y=550)
        self.weight_switch = Switch(self,"Weight in kg or lbs? \n(KG-LEFT, LBS-RIGHT)",x=390,y=630)
        self.height_switch = Switch(self,"Height in metres or inches? \n(METRES-LEFT, INCHES-RIGHT)",x=390,y=590)
        self.convertfrom_cm_label = Label(self, "Do you only know your\n height in cm or mm?\n convert your height into\n metres here:", x=90, y=430, font=self.convertfrom_cm_font)
        self.cm_to_m_label = Label(self, "cm to m:", x=20, y=500, font=self.header_font)
        self.mm_to_m_label = Label(self, "mm to m:", x=20, y=585, font=self.header_font)
        self.cm_to_m_entry = Entry(self, "", self.cm, x=120, y=500)
        self.mm_to_m_entry = Entry(self, "", self.mm, x=120, y=585)
        self.convert_mm_to_m_button = Button(self, "Convert", self.convert_mm_to_m, x=120, y=620)
        self.convert_cm_to_m_button = Button(self, "Convert", self.convert_cm_to_m, x=120, y=535)
        self.ethnicity_options = ComboBox(self,values = ["Prefer not to say","White","Mixed","Pakistani","Middle eastern","Indian","Chinese","Black caribbean","Black african","Bangladeshi","Other"],x=700,y=470)
        self.ethnicity_label = Label(self, "What is your ethnicity?", x=700, y=430, font=self.header_font)
        self.ethnicityexplanation_label = Label(self, "(We ask this because \nBMI results can vary for \ndifferent ethnic groups)", x=700, y=540, font=self.ethnicityexplanation_font)
        self.delete_button = Button(self, "Delete Account", self.delete_acccountbutton, x=20, y=80)
        self.bmigraph_label = Label(self, "When BMI is obtained, \na graph showing your \n data will appear\non the right→\n\nNote that BMI does not\ntake muscle mass into account\nso muscular athletes may\nbe classed as overweight", x=20, y=150, font=self.bmi_label_font)
        self.product_code_scanner = Button(self, "Product code scanner", self.product_scanner, x=160, y=20)
        self.manage_fitness_plans_button = Button(self, "Manage fitness plans", self.manage_fitness_plans, x=160, y=50)
        self.change_details_button = Button(self, "Change account\ndetails", self.change_account_details, x=750, y=20)
        self.close_app = Button(self, "Close app", self.close_app, x=160, y=80)

    #log out
    def logout(self):
        msg_box = messagebox.askquestion(title = "Logout", message = "Are you sure you want to log out?")
        if msg_box == "yes":
            call(["python","FitPro.py"])
            self.close_everything()

    #go to "deleteaccount" page
    def delete_acccountbutton(self):
        msg_box = messagebox.askquestion(title = "Delete account", message = "Are you sure you want to delete your account? \nIf you change your mind, you will have to log in again.")
        if msg_box == "yes":
            script_path = os.path.join("Scripts", "delete_account.py")
            subprocess.run(["python", script_path])
            self.close_everything()

    #go to "get_info" page to start creating plan process
    def create_plan(self):
        script_path = os.path.join("Scripts", "get_info.py")
        subprocess.run(["python", script_path])
        self.close_everything()

    #go to "foodapi" page
    def product_scanner(self):
        script_path = os.path.join("Scripts", "product_scanner.py")
        subprocess.run(["python", script_path])
        self.close_everything()

    #go to "manage_fitness_plans" page
    def manage_fitness_plans(self):
        script_path = os.path.join("Scripts", "manage_fitness_plans.py")
        subprocess.run(["python", script_path])
        self.close_everything()

    #go to "change_details" page
    def change_account_details(self):
        msg_box = messagebox.askquestion(title = "Change account details", message = "Are you sure you want to change your details? \nIf you change your mind, you will have to log in again.")
        if msg_box == "yes":
            script_path = os.path.join("Scripts", "change_details.py")
            call(["python",script_path])
            self.close_everything()
   
    #information for BMI calculator about ethnicity groups and BMI ranges is used from https://www.nhs.uk/live-well/healthy-weight/bmi-calculator/
    #(NHS page may have been updated so all required information may have changed)
    #when "Calculate"   button is pressed, check the value switches to see what units the user wants to use,
    #and check if input is a number or if entries are not empty, or else an error message will pop up
    def calculate_bmi(self):
        weight_input = self.weight_entry.get()
        height_input = self.height_entry.get()
        if (weight_input != "") and (height_input != ""):
            try:
                weight = float(weight_input)
                height = float(height_input)
                weightswitch_value = self.weight_switch.get()
                heightswitch_value = self.height_switch.get()
                if (weightswitch_value == 0) and (heightswitch_value == 0):
                    self.calculate_bmi_kg_m()
                elif (weightswitch_value == 1) and (heightswitch_value == 1):
                    self.calculate_bmi_lbs_inches()
                elif (weightswitch_value == 1) and (heightswitch_value == 0):
                    self.calculate_bmi_lbs_m()
                elif (weightswitch_value == 0) and (heightswitch_value == 1):
                    self.calculate_bmi_kg_inches()
            
            except ValueError:
                messagebox.showerror(title="Error", message="Weight and height must be numbers")
                self.weight_entry.delete(0,END)
                self.height_entry.delete(0,END)
        else:
            messagebox.showerror(title="Error", message="Weight or height cannot be empty")        
        self.weight_entry.delete(0,END)
        self.height_entry.delete(0,END)

    #convert inches to metres and calculate bmi
    def calculate_bmi_kg_inches(self):
        kg = float(self.weight_entry.get())
        inches = float(self.height_entry.get())
        m = inches / 39.37
        m_squared = m * m
        bmi = kg/m_squared
        self.result(bmi)

    #convert metres to inches and calculate bmi
    def calculate_bmi_lbs_m(self):
        lbs = float(self.weight_entry.get())
        m = float(self.height_entry.get())
        inches = m * 39.37
        bmi = (lbs/(inches*inches)) * 703
        self.result(bmi)

    #calculate bmi
    def calculate_bmi_kg_m(self):
        kg = float(self.weight_entry.get())
        m = float(self.height_entry.get())
        m_squared = m*m
        bmi = kg/m_squared
        self.result(bmi)

    #calculate bmi
    def calculate_bmi_lbs_inches(self):
        lbs = float(self.weight_entry.get())
        inches = float(self.height_entry.get())
        bmi = (lbs/(inches*inches)) * 703
        self.result(bmi) 

    #show result of BMI, also depending on ethicity option (e.g: underweight, overweight, healthy weight)
    def result(self,bmi):
        selected_value = self.ethnicity_options.get()
        underweight_border = 18.5
        overweight_border = 24.9
        obese_border = 30
        #adjust borders based on user's ethicity choice
        if selected_value not in ["White", "Prefer not to say"]:
            overweight_border = 23
            obese_border = 27.5
        #work out the result based off the user's bmi
        if underweight_border <= bmi <= overweight_border:
            weight_result = "a healthy weight"
        elif bmi < underweight_border:
            weight_result = "underweight"
        elif bmi > obese_border:
            weight_result = "obese"
        else:
            weight_result = "overweight"
        #Display result to user to show if they are a healthy weight, underweight, overweight or obese
        messagebox.showinfo(title = "Success", message = f"Your BMI is {(bmi)}, you are {(weight_result)}. \nTo ensure that you have the correct result, please make sure to check your units.")
        #call function to display graph based on user's result for data visualisation
        self.display_bmi_graph(bmi)

    #this website was used to find the horizontal bar graph from matplotlib: https://matplotlib.org/stable/gallery/lines_bars_and_markers/barh.html#sphx-glr-gallery-lines-bars-and-markers-barh-py
    #these videos were used to learn how to use matplotlib and how to integrate it into Tkinter: https://www.youtube.com/watch?v=2JjQIh-sgHU&t=9s
    #https://www.youtube.com/watch?v=8exB6Ly3nx0
    #create a horizontal bar graph Based on the user's BMI
    def display_bmi_graph(self,bmi):
        selected_value = self.ethnicity_options.get()
        #onstruct graph by labelling axis, and by creating the bars (by choosing colours and width of bars)
        categories = ["Your BMI", "Underweight", "Optimal\nweight", "Overweight", "Obese"]
        borders = [bmi, 18.5, 21.7, 24.9, 30]
        #adjust borders based on user's ethicity choice
        if selected_value not in ["White", "Prefer not to say"]:
            borders = [bmi, 18.5, 20.75, 23, 27.5]
        colours = ['skyblue', 'red', 'green', 'yellow', 'orange']
        plt.clf()
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_xlabel("BMI Value")
        ax.barh(categories, borders, color=colours)
        #create title of graph
        ax.set_title("BMI Chart")
        #specify width of graph
        ax.set_xlim(0, max(borders)) 
        #add grid lines for better readibility 
        ax.grid(axis='x')
        #place graph on window
        canvas = FigureCanvasTkAgg(fig, master=self)
        bmi_graph = canvas.get_tk_widget()
        bmi_graph.place(x=540, y=125)


    #convert cm to m and display result
    def convert_cm_to_m(self):
        input_cm = self.cm.get()
        if input_cm != "":
            try:
                input_cm = float(input_cm)
                m = float(input_cm)/100
                messagebox.showinfo(title="Success", message = f"{float(input_cm)} cm is {float(m)} m")
                self.cm_to_m_entry.delete(0,END)
            except ValueError:
                messagebox.showerror(title = "Error", message = "cm must be a number")
                self.cm_to_m_entry.delete(0,END)
        else:
            messagebox.showerror(title = "Error",message="cm to m cannot be empty")

    #convert mm to m and display result
    def convert_mm_to_m(self):
        input_mm = self.mm.get()
        if input_mm != "":
            try:
                input_mm = float(input_mm)
                m = float(input_mm)/1000
                messagebox.showinfo(title="Success", message = f"{float(input_mm)} mm is {float(m)} m")
                self.mm_to_m_entry.delete(0,END)
            except ValueError:
                messagebox.showerror(title = "Error", message = "mm must be a number")
                self.mm_to_m_entry.delete(0,END)
        else:
            messagebox.showerror(title = "Error",message="mm to m cannot be empty")

    def close_app(self):
        msg_box = messagebox.askquestion(title = "Close App", message = "Are you sure you want to close the app?")
        if msg_box == "yes":
            self.close_everything()
    
    def close_everything(self):
        children = self.winfo_children()
        for widget in children:
            widget.destroy()
        self.quit()
        #for some reason the script does not get fully terminated only if I close window or go to another page after the graph has been created and placed,
        #so i would have to restart my IDE just to run the script again for testing
        #I used sys.exit() to fully terminate the script and to solve this issue, I found it here: https://stackoverflow.com/questions/73663/how-do-i-terminate-a-script
        sys.exit()   

#run window
if __name__ == "__main__":
    app = window()
    app.mainloop()

#There is a lot of code in this script to handle all possible outcomes incase they happen,
#but every time this code is run, (compared to all of the code) only a small amount will be run,
#This is because of the many if statements and conditions in this script
#I was able to write this code by re-using a lot of it and adjusting it
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
from tkinter import font
import os
import sqlite3

import subprocess
from subprocess import call

#class to create font
class Font(ctk.CTkFont):
    def __init__(self, family, size, weight):
        super().__init__(family=family, size=size, weight=weight)
#class to create widgets
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
        #create window
        self.title("FitPro")
        self.geometry("500x300")
        self.resizable(False, False)
        #this will call method that will discard information if user presses close button in top right corner
        self.protocol("WM_DELETE_WINDOW", self.discard_on_close)

        #collect plan name from user
        self.plan_name_var = StringVar()
        #create font for label
        self.header_font = Font("Helvetica", 16, "bold")

        #create and place widgets
        self.discard_button = Button(self, "Discard plan", self.discard, x=10, y=10)
        self.explanation_label = Label(self,"Enter the name of your plan\n and we will create it for you.",self.header_font,x=200,y=20)
        self.plan_name_label = Label(self,"Enter plan name here:",self.header_font,x=40,y=120)
        self.plan_name_entry = Entry(self,"",self.plan_name_var,x=220,y=120)
        self.create_button = Button(self, "create plan", self.create_plan, x=220,y=150)

    def create_plan(self):
        #collect current date of fitness plan creation and the plan name, 
        #and it will create the primary key for plan_identification, 
        #and insert it into all of the other linked tables as a foreign key, 
        #and it will also insert the user's account key into the plan_identification table

        #get user's account key
        with open("Scripts/user_account_key.txt","r") as f:
                self.account_key = f.readline()
        current_day = datetime.now()
        current_date = current_day.date()
        plan_name = self.plan_name_var.get()
        plan_name_length = len(plan_name)
        #check if the user has not entered nothing
        if plan_name != "":
            #check if plan name is not too long
            if plan_name_length <= 20:
                try:
                    #make plan entry
                    conn = sqlite3.connect("information.db")
                    cur = conn.cursor()
                    cur.execute("INSERT INTO plan_identification (plan_name, start_date) VALUES (?, ?)", (plan_name, current_date.isoformat()))

                    #get plan key
                    cur.execute("SELECT MAX(id) FROM plan_identification")
                    plan_key_tuple = cur.fetchone()
                    self.plan_key = plan_key_tuple[0]
                    #add user's account key and plan key to plan identification table
                    cur.execute("UPDATE plan_identification SET user_fk = ? WHERE id = ?", (self.account_key, self.plan_key))
                    #get most recent entry of information from one of the information tables
                    cur.execute("SELECT MAX(main_id) FROM user_personal_info")
                    information_id = cur.fetchone()
                    most_recent_entry = information_id[0]
                    #add user's account key and plan key to user personal info and equipment access tables
                    cur.execute("UPDATE user_personal_info SET id = ? WHERE main_id = ?", (self.plan_key,most_recent_entry))
                    cur.execute("UPDATE equipment_access SET id = ? WHERE main_id = ?", (self.plan_key,most_recent_entry))
                    conn.commit()
                    conn.close()
                    #write plan key to file so it can be used to display the plan
                    #access subfolder, so the text file gets written to inside the subfolder, 
                    #and so it does not get created outside the subfolder, for better file organisation
                    with open("Scripts/user_plan_key.txt","w") as file:
                        file.write(str(self.plan_key))
                    self.get_info()
                #use of unique constraint to prevent duplicate plan names
                except sqlite3.IntegrityError:
                    #close connection here so database does not lock out
                    conn.close()
                    messagebox.showerror(title = "Error", message = "Plan name already exists in the database")
                except sqlite3.OperationalError as e:
                    print(e)
            else:
                messagebox.showerror(title = "Error", message = "Plan name is too long")
                self.plan_name_entry.delete(0,END)
        else:
            messagebox.showerror(title = "Error", message = "plan name entry must not be empty")
            self.plan_name_entry.delete(0,END)

    #This method will collect all personal information from the user
    def get_info(self):
        conn = sqlite3.connect("information.db")
        cur = conn.cursor()
        cur.execute("""
            SELECT *
            FROM equipment_access
            WHERE user_fk = ?   -- select correct user
            ORDER BY id DESC    -- select most recent entry
            LIMIT 1
        """, (self.account_key,))
        equipment_access = cur.fetchone() 
        cur.execute("""
            SELECT *
            FROM user_personal_info
            WHERE user_fk = ?  -- select correct user
            ORDER BY id DESC   -- select most recent entry
            LIMIT 1
        """, (self.account_key,))
        user_personal_info = cur.fetchone()
        conn.close()
        #get information from user_personal_info table
        self.current_weight = user_personal_info[3]
        self.weight_goal = user_personal_info[4]
        self.physical_activity = user_personal_info[5]
        self.workout_type = user_personal_info[6]
        self.gym_access = user_personal_info[7]
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

        #Lists of tuples are used to store exercise data that will be inserted into the plan
        #For all tuples apart from cardio and core, first column is the exercise, 
        #I sorted the exercises in the order of how effective they are, based on research and my opinions
        #they are also sorted in a way that the for loop can access all exercises if needed, 
        #so it will go through the exercises first that require equipment, and if the user does not have access to those exercises,
        #the exercises that require no equipment will be selected
        #first column is the exercise name,
        #second column is the exercise day, 
        #third column is the muscle group the exercise is targeting, 
        #fourth row is whether equipment is needed

        #list of tuples of upper body exercises (isolation exercises)
        self.upper_body_exercises = [
            #use OR AND for equipment row
            ("Preacher curls", "Pull", "biceps", (self.ez_bar and self.preacher_curl_bench)),
            ("Incline bicep\ncurls","Pull","biceps",(self.dumbells and self.bench)),
            ("Incline hammer\ncurls","Pull","biceps",(self.dumbells and self.bench)),
            ("Lateral raise", "Push", "shoulders", (self.dumbells or self.cables)),
            ("Tricep press", "Push", "triceps", self.tricep_press_machine),
            ("Rear delts", "Push", "shoulders", (self.cables or self.pec_fly_machine)),
            ("Bicep curls", "Pull", "biceps", self.dumbells),
            ("Hammer curls", "Pull", "biceps", self.dumbells),
            ("Barbell curls", "Pull", "biceps", self.barbell),
            ("Tricep extensions\nwith ez bar", "Push", "triceps", self.ez_bar),
            ("Tricep extensions\nwith cables", "Push", "triceps", self.cables),
            ("Tricep extensions\nwith dumbells", "Push", "triceps", self.dumbells),
            ("Reverse snow angels\n(using heavy objects)", "Pull", "biceps", None),
            ("Isometric hold", "Push", "shoulders", None),
            ("Superman pull", "Pull", "biceps", None),
            ("Chest squeeze", "Push", "shoulders", None),
            ("Wall push ups", "Push", "shoulders", None),
            ("Isometric shoulder\nretraction", "Pull", "biceps", None)
        ]

        #list of tuples of lower body exercises (isolation exercises)
        self.lower_body_exercises = [
            ("Leg extensions", "Legs", "legs", self.leg_extensions_machine),
            ("Leg curls", "Legs", "legs", self.leg_curl_machine),
            ("Calf raises", "Legs", "legs", None),
            ("Glute bridges", "Legs", "legs", None),
            ("Standing lateral\nleg raise", "Legs", "legs", None)
        ]

        #list of tuples of compound exercises
        self.compound_exercises = [
            ("Pull ups", "Pull", "back,shoulders,biceps", self.pull_up_bar),
            ("Dips", "Push", "triceps,chest", self.dip_station),
            ("Chin ups","Pull","back,shoulders,biceps",self.pull_up_bar),
            ("Deadlift","Legs,Pull","back,legs",self.barbell),
            ("Bench press","Push","chest,shoulders,triceps",(self.barbell and self.bench)),
            ("Shoulder press","Push","shoulders,triceps,chest",self.shoulder_press_machine),
            ("Laterall pull-down","Pull","back,shoulder,biceps",self.lateral_pulldown_machine),
            ("Pec fly","Push","shoulders,triceps,biceps",self.pec_fly_machine),
            ("Rows","Pull","shoulders,back,biceps",(self.rowing_machine or self.cables)),
            ("Leg press","Legs","legs",(self.leg_press_machine)),
            ("Bulgarian split squat","Legs","legs",(self.bench and self.dumbells)),
            ("Pull ups\n(using fridge)", "Pull", "back,shoulders,biceps", None),
            ("Burpees","Legs,Push","chest,triceps,shoulders,legs",None),
            ("Lunges","Legs","legs",None),
            ("Push ups","Push","triceps,chest,shoulders",None),
            ("Inverted rows\n(using table)", "Pull", "back,shoulders,biceps", None),
            ("Squats", "Legs", "legs", None)
        ]

        #list of tuples of cardio exercises
        #for list of tuples of cardio exercises, first column is the exercise
        #and second column is whether equipment is needed
        self.cardio_exercises = [
            ("Running on\ntreadmill", self.treadmill),
            ("Biking", self.exercise_bike),
            ("Stairmaster",self.stair_climber_machine),
            ("Skipping rope", self.skipping_rope),
            ("Crunches", None)
        ]
        #call method to create plan
        self.create_plan_details()

    #This method will check what the user's weight goal is,
    #then go to the correct method to create the plan
    def create_plan_details(self):
        if self.current_weight > self.weight_goal:
            self.lose_weight()
        elif self.current_weight < self.weight_goal:
            self.build_lean_muscle()
        elif self.current_weight == self.weight_goal:
            self.maintain_weight()
                
    #one of these three methods will create a blueprint for what the workout plan should consist of
    #For the workout structure, based on my research and opinions, I have structured the workout in this way so that it will
    #start with compound exercise(s), then have isolation exercises, then have cardio to finish the workout, so the user will 
    #not neglect cardiovascular health

    #The structure for all of this code is the same throughout and it repeats, just with different numbers and variables so I will explan each new loop once, 
    #and the understanding can be applied to all of the remaining code
    def lose_weight(self):
        self.push_day1 = []
        self.pull_day1 = []
        self.legs_day1 = []
    #sets the correct number of exercises based on the user's past fitness experience
        if self.physical_activity == "low":
            #max_exercises_per_day is there for testing purposes as an indicator of how many exercises should be in each list
            max_exercises_per_day = 4
            compound_exercises_per_day = 2
            isolation_exercises_per_day = 1
            cardio_exercises_per_day = 1
            
        elif self.physical_activity == "moderate":
            max_exercises_per_day = 5
            compound_exercises_per_day = 2
            isolation_exercises_per_day = 2
            cardio_exercises_per_day = 1

        else:
            max_exercises_per_day = 6
            compound_exercises_per_day = 2
            isolation_exercises_per_day = 3
            cardio_exercises_per_day = 1
        #set counters so loop can end
        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add compound exercises to push day
        for exercise in self.compound_exercises:
            #check if exercise is the correct exercise day and if the user has the correct equipment access
            #also check if stopping condition has been reached by comparing the counter with its corresponding exercise day
            if compound_counter < compound_exercises_per_day and "Push" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                #add to list if requirements are satisfied
                self.push_day1.append(exercise[0])
                #increment counter
                compound_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add isolation exercises to push day
        for exercise in self.upper_body_exercises:
            if isolation_counter < isolation_exercises_per_day and "Push" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.push_day1.append(exercise[0])
                isolation_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add cardio exercises to push day
        for exercise in self.cardio_exercises:
            if cardio_counter < cardio_exercises_per_day and (exercise[1] == 1 or exercise[1]==None):
                self.push_day1.append(exercise[0])
                cardio_counter += 1
        
        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add compound exercises to pull day
        for exercise in self.compound_exercises:
            if compound_counter < compound_exercises_per_day and "Pull" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.pull_day1.append(exercise[0])
                compound_counter += 1
        
        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add isolation exercises to pull day
        for exercise in self.upper_body_exercises:
            if isolation_counter < isolation_exercises_per_day and "Pull" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.pull_day1.append(exercise[0])
                isolation_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add cardio exercises to pull day
        for exercise in self.cardio_exercises:
            if cardio_counter < cardio_exercises_per_day and (exercise[1] == 1 or exercise[1]==None):
                self.pull_day1.append(exercise[0])
                cardio_counter += 1
        
        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add compound exercises to legs day
        for exercise in self.compound_exercises:
            if compound_counter < compound_exercises_per_day and "Legs" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.legs_day1.append(exercise[0])
                compound_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add isolation exercises to legs day
        for exercise in self.lower_body_exercises:
            if isolation_counter < isolation_exercises_per_day and "Legs" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.legs_day1.append(exercise[0])
                isolation_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add compound exercises to legs day
        for exercise in self.cardio_exercises:
            if cardio_counter < cardio_exercises_per_day and (exercise[1] == 1 or exercise[1]==None):
                self.legs_day1.append(exercise[0])
                cardio_counter += 1

        #if user wants a balanced workout plan, the plan will stay the same as it is, but if the user wants focus on a specific muscle group,
        #an extra isolation exercise will get added into the other exercise which will target that muscle group
        if self.workout_type != "Balanced":
            if self.workout_type == "Focus on legs" and self.physical_activity == "low":
                legs_exercise = None
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        legs_exercise = exercise[0]
                        y += 1
                self.push_day1[2] = legs_exercise
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:                                              #makes sure that different exercises get added
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and legs_exercise != exercise[0]:
                        legs_exercise = exercise[0]
                        y += 1
                self.pull_day1[2] = legs_exercise
                
            elif self.workout_type == "Focus on legs" and self.physical_activity == "moderate":
                legs_exercise = None
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        legs_exercise = exercise[0]
                        y += 1
                self.push_day1[3] = legs_exercise
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and legs_exercise != exercise[0]:
                        legs_exercise = exercise[0]
                        y += 1
                self.pull_day1[3] = legs_exercise

            elif self.workout_type == "Focus on legs" and self.physical_activity == "vigorous":
                legs_exercise = None
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        legs_exercise = exercise[0]
                        y += 1
                self.push_day1[4] = legs_exercise
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and legs_exercise != exercise[0]:
                        legs_exercise = exercise[0]
                        y += 1
                self.pull_day1[4] = legs_exercise

            elif self.workout_type == "Focus on back" and self.physical_activity == "low":
                back_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        back_exercise = exercise[0]
                        y += 1
                self.push_day1[2] = back_exercise
                x = 1
                y = 0
                for exercise in self.compound_body_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and back_exercise != exercise[0]:
                        back_exercise = exercise[0]
                        y += 1
                self.legs_day1[2] = back_exercise

            elif self.workout_type == "Focus on back" and self.physical_activity == "moderate":
                back_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        back_exercise = exercise[0]
                        y += 1
                self.push_day1[3] = back_exercise
                x = 1
                y = 0
                for exercise in self.compound_body_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and back_exercise != exercise[0]:
                        back_exercise = exercise[0]
                        y += 1
                self.legs_day1[3] = back_exercise

            elif self.workout_type == "Focus on back" and self.physical_activity == "vigorous":
                back_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        back_exercise = exercise[0]
                        y += 1
                self.push_day1[4] = back_exercise
                x = 1
                y = 0
                for exercise in self.compound_body_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and back_exercise != exercise[0]:
                        back_exercise = exercise[0]
                        y += 1
                self.legs_day1[4] = back_exercise

            elif self.workout_type == "Focus on biceps" and self.physical_activity == "low":
                biceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        biceps_exercise = exercise[0]
                        y += 1
                self.push_day1[2] = biceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and biceps_exercise != exercise[0]:
                        biceps_exercise = exercise[0]
                        y += 1
                self.legs_day1[2] = biceps_exercise

            elif self.workout_type == "Focus on biceps" and self.physical_activity == "moderate":
                biceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        biceps_exercise = exercise[0]
                        y += 1
                self.push_day1[3] = biceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and biceps_exercise != exercise[0]:
                        biceps_exercise = exercise[0]
                        y += 1
                self.legs_day1[3] = biceps_exercise

            elif self.workout_type == "Focus on biceps" and self.physical_activity == "vigorous":
                biceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        biceps_exercise = exercise[0]
                        y += 1
                self.push_day1[4] = biceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and biceps_exercise != exercise[0]:
                        biceps_exercise = exercise[0]
                        y += 1
                self.legs_day1[4] = biceps_exercise

            elif self.workout_type == "Focus on triceps" and self.physical_activity == "low":
                triceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        triceps_exercise = exercise[0]
                        y += 1
                self.pull_day1[2] = triceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and triceps_exercise != exercise[0]:
                        triceps_exercise = exercise[0]
                        y += 1
                self.legs_day1[2] = triceps_exercise
                if None in self.pull_day1:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                            triceps_exercise = exercise[0]
                            y += 1
                    self.pull_day1[2] = triceps_exercise

                if None in self.legs_day1:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and exercise[0] != triceps_exercise:
                            triceps_exercise = exercise[0]
                            y += 1
                    self.legs_day1[2] = triceps_exercise


            elif self.workout_type == "Focus on triceps" and self.physical_activity == "moderate":
                triceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        triceps_exercise = exercise[0]
                        y += 1
                self.pull_day1[3] = triceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and triceps_exercise != exercise[0]:
                        triceps_exercise = exercise[0]
                        y += 1
                self.legs_day1[3] = triceps_exercise

                if None in self.pull_day1:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                            triceps_exercise = exercise[0]
                            y += 1
                    self.pull_day1[3] = triceps_exercise

                if None in self.legs_day1:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and exercise[0] != triceps_exercise:
                            triceps_exercise = exercise[0]
                            y += 1
                self.legs_day1[3] = triceps_exercise

            elif self.workout_type == "Focus on triceps" and self.physical_activity == "vigorous":
                triceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        triceps_exercise = exercise[0]
                        y += 1
                self.pull_day1[4] = triceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and triceps_exercise != exercise[0]:
                        triceps_exercise = exercise[0]
                        y += 1
                self.legs_day1[4] = triceps_exercise

                if None in self.pull_day1:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                            triceps_exercise = exercise[0]
                            y += 1
                    self.pull_day1[4] = triceps_exercise
                    
                if None in self.legs_day1:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and exercise[0] != triceps_exercise:
                            triceps_exercise = exercise[0]
                            y += 1
                self.legs_day1[4] = triceps_exercise

            elif self.workout_type == "Focus on shoulders" and self.physical_activity == "low":
                shoulders_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.pull_day1[2] = shoulders_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and shoulders_exercise != exercise[0]:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.legs_day1[2] = shoulders_exercise

            elif self.workout_type == "Focus on shoulders" and self.physical_activity == "moderate":
                shoulders_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.pull_day1[3] = shoulders_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and shoulders_exercise != exercise[0]:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.legs_day1[3] = shoulders_exercise

            elif self.workout_type == "Focus on shoulders" and self.physical_activity == "vigorous":
                shoulders_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.pull_day1[4] = shoulders_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and shoulders_exercise != exercise[0]:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.legs_day1[4] = shoulders_exercise

            elif self.workout_type == "Focus on chest" and self.physical_activity == "low":
                chest_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        chest_exercise = exercise[0]
                        y += 1
                self.pull_day1[2] = chest_exercise
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and chest_exercise != exercise[0]:
                        chest_exercise = exercise[0]
                        y += 1
                self.legs_day1[2] = chest_exercise

            elif self.workout_type == "Focus on chest" and self.physical_activity == "moderate":
                chest_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        chest_exercise = exercise[0]
                        y += 1
                self.pull_day1[3] = chest_exercise
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and chest_exercise != exercise[0]:
                        chest_exercise = exercise[0]
                        y += 1
                self.legs_day1[3] = chest_exercise

            elif self.workout_type == "Focus on chest" and self.physical_activity == "vigorous":
                chest_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        chest_exercise = exercise[0]
                        y += 1
                self.pull_day1[4] = chest_exercise
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and chest_exercise != exercise[0]:
                        chest_exercise = exercise[0]
                        y += 1
                self.legs_day1[4] = chest_exercise
            
            elif self.workout_type == "Focus on cardio" and self.physical_activity == "low":
                cardio_exercise = None
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x:
                        cardio_exercise = exercise[0]
                        y += 1
                self.pull_day1[2] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.legs_day1[2] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.push_day1[2] = cardio_exercise

            elif self.workout_type == "Focus on cardio" and self.physical_activity == "moderate":
                cardio_exercise = None
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x:
                        cardio_exercise = exercise[0]
                        y += 1
                self.pull_day1[3] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.legs_day1[3] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.push_day1[3] = cardio_exercise

            elif self.workout_type == "Focus on cardio" and self.physical_activity == "vigorous":
                cardio_exercise = None
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x:
                        cardio_exercise = exercise[0]
                        y += 1
                self.pull_day1[4] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.legs_day1[4] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.push_day1[4] = cardio_exercise
        #workout plan doesn't get changed if user wants a balanced workout
        else:
            pass

        self.insert_information()

    def build_lean_muscle(self):
        self.push_day2 = []
        self.pull_day2 = []
        self.legs_day2 = []

        if self.physical_activity == "low":
            max_exercises_per_day = 4
            compound_exercises_per_day = 1
            isolation_exercises_per_day = 2
            cardio_exercises_per_day = 1
            
        elif self.physical_activity == "moderate":
            max_exercises_per_day = 5
            compound_exercises_per_day = 1
            isolation_exercises_per_day = 3
            cardio_exercises_per_day = 1

        else:
            max_exercises_per_day = 6
            compound_exercises_per_day = 2
            isolation_exercises_per_day = 3
            cardio_exercises_per_day = 1
        #counters so loop can end
        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add compound exercises to push day
        for exercise in self.compound_exercises:
            if compound_counter < compound_exercises_per_day and "Push" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.push_day2.append(exercise[0])
                compound_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add isolation exercises to push day
        for exercise in self.upper_body_exercises:
            if isolation_counter < isolation_exercises_per_day and "Push" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.push_day2.append(exercise[0])
                isolation_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add cardio exercises to push day
        for exercise in self.cardio_exercises:
            if cardio_counter < cardio_exercises_per_day and (exercise[1] == 1 or exercise[1]==None):
                self.push_day2.append(exercise[0])
                cardio_counter += 1
        
        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add compound exercises to pull day
        for exercise in self.compound_exercises:
            if compound_counter < compound_exercises_per_day and "Pull" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.pull_day2.append(exercise[0])
                compound_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add isolation exercises to pull day
        for exercise in self.upper_body_exercises:
            if isolation_counter < isolation_exercises_per_day and "Pull" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.pull_day2.append(exercise[0])
                isolation_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add cardio exercises to pull day
        for exercise in self.cardio_exercises:
            if cardio_counter < cardio_exercises_per_day and (exercise[1] == 1 or exercise[1]==None):
                self.pull_day2.append(exercise[0])
                cardio_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add compound exercises to legs day
        for exercise in self.compound_exercises:
            if compound_counter < compound_exercises_per_day and "Legs" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.legs_day2.append(exercise[0])
                compound_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add isolation exercises to legs day
        for exercise in self.lower_body_exercises:
            if isolation_counter < isolation_exercises_per_day and "Legs" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.legs_day2.append(exercise[0])
                isolation_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add compound exercises to legs day
        for exercise in self.cardio_exercises:
            if cardio_counter < cardio_exercises_per_day and (exercise[1] == 1 or exercise[1]==None):
                self.legs_day2.append(exercise[0])
                cardio_counter += 1

        #if user wants a balanced workout plan, the plan will stay the same as it is, but if the user wants focus on a specific muscle group,
        #an extra isolation exercise will get added into the other exercise which will target that muscle group
        if self.workout_type != "Balanced":
            if self.workout_type == "Focus on legs" and self.physical_activity == "low":
                legs_exercise = None
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        legs_exercise = exercise[0]
                        y += 1
                self.push_day2[2] = legs_exercise
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:                           #makes sure that different exercises get added
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and legs_exercise != exercise[0]:
                        legs_exercise = exercise[0]
                        y += 1
                self.pull_day2[2] = legs_exercise
                
            elif self.workout_type == "Focus on legs" and self.physical_activity == "moderate":
                legs_exercise = None
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        legs_exercise = exercise[0]
                        y += 1
                self.push_day2[3] = legs_exercise
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and legs_exercise != exercise[0]:
                        legs_exercise = exercise[0]
                        y += 1
                self.pull_day2[3] = legs_exercise

            elif self.workout_type == "Focus on legs" and self.physical_activity == "vigorous":
                legs_exercise = None
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        legs_exercise = exercise[0]
                        y += 1
                self.push_day2[4] = legs_exercise
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and legs_exercise != exercise[0]:
                        legs_exercise = exercise[0]
                        y += 1
                self.pull_day2[4] = legs_exercise

            elif self.workout_type == "Focus on back" and self.physical_activity == "low":
                back_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        back_exercise = exercise[0]
                        y += 1
                self.push_day2[2] = back_exercise
                x = 1
                y = 0
                for exercise in self.compound_body_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and back_exercise != exercise[0]:
                        back_exercise = exercise[0]
                        y += 1
                self.legs_day2[2] = back_exercise

            elif self.workout_type == "Focus on back" and self.physical_activity == "moderate":
                back_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        back_exercise = exercise[0]
                        y += 1
                self.push_day2[3] = back_exercise
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and back_exercise != exercise[0]:
                        back_exercise = exercise[0]
                        y += 1
                self.legs_day2[3] = back_exercise

            elif self.workout_type == "Focus on back" and self.physical_activity == "vigorous":
                back_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        back_exercise = exercise[0]
                        y += 1
                self.push_day2[4] = back_exercise
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and back_exercise != exercise[0]:
                        back_exercise = exercise[0]
                        y += 1
                self.legs_day2[4] = back_exercise

            elif self.workout_type == "Focus on biceps" and self.physical_activity == "low":
                biceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        biceps_exercise = exercise[0]
                        y += 1
                self.push_day2[2] = biceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and biceps_exercise != exercise[0]:
                        biceps_exercise = exercise[0]
                        y += 1
                self.legs_day2[2] = biceps_exercise

            elif self.workout_type == "Focus on biceps" and self.physical_activity == "moderate":
                biceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        biceps_exercise = exercise[0]
                        y += 1
                self.push_day2[3] = biceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and biceps_exercise != exercise[0]:
                        biceps_exercise = exercise[0]
                        y += 1
                self.legs_day2[3] = biceps_exercise

            elif self.workout_type == "Focus on biceps" and self.physical_activity == "vigorous":
                biceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        biceps_exercise = exercise[0]
                        y += 1
                self.push_day2[4] = biceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and biceps_exercise != exercise[0]:
                        biceps_exercise = exercise[0]
                        y += 1
                self.legs_day2[4] = biceps_exercise

            elif self.workout_type == "Focus on triceps" and self.physical_activity == "low":
                triceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        triceps_exercise = exercise[0]
                        y += 1
                self.pull_day2[2] = triceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and triceps_exercise != exercise[0]:
                        triceps_exercise = exercise[0]
                        y += 1
                self.legs_day2[2] = triceps_exercise
                if None in self.pull_day2:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                            triceps_exercise = exercise[0]
                            y += 1
                    self.pull_day1[2] = triceps_exercise

                if None in self.legs_day2:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and exercise[0] != triceps_exercise:
                            triceps_exercise = exercise[0]
                            y += 1
                    self.legs_day2[2] = triceps_exercise


            elif self.workout_type == "Focus on triceps" and self.physical_activity == "moderate":
                triceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        triceps_exercise = exercise[0]
                        y += 1
                self.pull_day2[3] = triceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and triceps_exercise != exercise[0]:
                        triceps_exercise = exercise[0]
                        y += 1
                self.legs_day2[3] = triceps_exercise

                if None in self.pull_day2:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                            triceps_exercise = exercise[0]
                            y += 1
                    self.pull_day2[3] = triceps_exercise

                if None in self.legs_day2:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and exercise[0] != triceps_exercise:
                            triceps_exercise = exercise[0]
                            y += 1
                self.legs_day2[3] = triceps_exercise

            elif self.workout_type == "Focus on triceps" and self.physical_activity == "vigorous":
                triceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        triceps_exercise = exercise[0]
                        y += 1
                self.pull_day2[4] = triceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and triceps_exercise != exercise[0]:
                        triceps_exercise = exercise[0]
                        y += 1
                self.legs_day2[4] = triceps_exercise

                if None in self.pull_day2:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                            triceps_exercise = exercise[0]
                            y += 1
                    self.pull_day2[4] = triceps_exercise
                    
                if None in self.legs_day2:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and exercise[0] != triceps_exercise:
                            triceps_exercise = exercise[0]
                            y += 1
                self.legs_day2[4] = triceps_exercise

            elif self.workout_type == "Focus on shoulders" and self.physical_activity == "low":
                shoulders_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.pull_day2[2] = shoulders_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and shoulders_exercise != exercise[0]:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.legs_day2[2] = shoulders_exercise

            elif self.workout_type == "Focus on shoulders" and self.physical_activity == "moderate":
                shoulders_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.pull_day2[3] = shoulders_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and shoulders_exercise != exercise[0]:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.legs_day2[3] = shoulders_exercise

            elif self.workout_type == "Focus on shoulders" and self.physical_activity == "vigorous":
                shoulders_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.pull_day2[4] = shoulders_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and shoulders_exercise != exercise[0]:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.legs_day2[4] = shoulders_exercise

            elif self.workout_type == "Focus on chest" and self.physical_activity == "low":
                chest_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        chest_exercise = exercise[0]
                        y += 1
                self.pull_day2[2] = chest_exercise
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and chest_exercise != exercise[0]:
                        chest_exercise = exercise[0]
                        y += 1
                self.legs_day2[2] = chest_exercise

            elif self.workout_type == "Focus on chest" and self.physical_activity == "moderate":
                chest_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        chest_exercise = exercise[0]
                        y += 1
                self.pull_day2[3] = chest_exercise
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and chest_exercise != exercise[0]:
                        chest_exercise = exercise[0]
                        y += 1
                self.legs_day2[3] = chest_exercise

            elif self.workout_type == "Focus on chest" and self.physical_activity == "vigorous":
                chest_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        chest_exercise = exercise[0]
                        y += 1
                self.pull_day2[4] = chest_exercise
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and chest_exercise != exercise[0]:
                        chest_exercise = exercise[0]
                        y += 1
                self.legs_day2[4] = chest_exercise
            
            elif self.workout_type == "Focus on cardio" and self.physical_activity == "low":
                cardio_exercise = None
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x:
                        cardio_exercise = exercise[0]
                        y += 1
                self.pull_day2[2] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.legs_day2[2] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.push_day2[2] = cardio_exercise

            elif self.workout_type == "Focus on cardio" and self.physical_activity == "moderate":
                cardio_exercise = None
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x:
                        cardio_exercise = exercise[0]
                        y += 1
                self.pull_day2[3] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.legs_day2[3] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.push_day2[3] = cardio_exercise

            elif self.workout_type == "Focus on cardio" and self.physical_activity == "vigorous":
                cardio_exercise = None
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x:
                        cardio_exercise = exercise[0]
                        y += 1
                self.pull_day2[4] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.legs_day2[4] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.push_day2[4] = cardio_exercise
        #workout plan doesn't get changed if user wants a balanced workout
        else:
            pass

        self.insert_information()

    def maintain_weight(self):
        self.push_day3 = []
        self.pull_day3 = []
        self.legs_day3 = []

        if self.physical_activity == "low":
            max_exercises_per_day = 4
            compound_exercises_per_day = 1
            isolation_exercises_per_day = 2
            cardio_exercises_per_day = 1

        elif self.physical_activity == "moderate":
            max_exercises_per_day = 5
            compound_exercises_per_day = 2
            isolation_exercises_per_day = 2
            cardio_exercises_per_day = 1

        else:
            max_exercises_per_day = 6
            compound_exercises_per_day = 2
            isolation_exercises_per_day = 3
            cardio_exercises_per_day = 1
        #counters so loop can end
        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add compound exercises to push day
        for exercise in self.compound_exercises:
            if compound_counter < compound_exercises_per_day and "Push" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.push_day3.append(exercise[0])
                compound_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add isolation exercises to push day
        for exercise in self.upper_body_exercises:
            if isolation_counter < isolation_exercises_per_day and "Push" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.push_day3.append(exercise[0])
                isolation_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add cardio exercises to push day
        for exercise in self.cardio_exercises:
            if cardio_counter < cardio_exercises_per_day and (exercise[1] == 1 or exercise[1]==None):
                self.push_day3.append(exercise[0])
                cardio_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add compound exercises to pull day
        for exercise in self.compound_exercises:
            if compound_counter < compound_exercises_per_day and "Pull" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.pull_day3.append(exercise[0])
                compound_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add isolation exercises to pull day
        for exercise in self.upper_body_exercises:
            if isolation_counter < isolation_exercises_per_day and "Pull" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.pull_day3.append(exercise[0])
                isolation_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add cardio exercises to pull day
        for exercise in self.cardio_exercises:
            if cardio_counter < cardio_exercises_per_day and (exercise[1] == 1 or exercise[1]==None):
                self.pull_day3.append(exercise[0])
                cardio_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add compound exercises to legs day
        for exercise in self.compound_exercises:
            if compound_counter < compound_exercises_per_day and "Legs" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.legs_day3.append(exercise[0])
                compound_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add isolation exercises to legs day
        for exercise in self.lower_body_exercises:
            if isolation_counter < isolation_exercises_per_day and "Legs" in exercise[1] and (exercise[3] == 1 or exercise[3]==None):
                self.legs_day3.append(exercise[0])
                isolation_counter += 1

        compound_counter=0
        isolation_counter = 0
        cardio_counter = 0
        #add compound exercises to legs day
        for exercise in self.cardio_exercises:
            if cardio_counter < cardio_exercises_per_day and (exercise[1] == 1 or exercise[1]==None):
                self.legs_day3.append(exercise[0])
                cardio_counter += 1

        #if user wants a balanced workout plan, the plan will stay the same as it is, but if the user wants focus on a specific muscle group,
        #an extra isolation exercise will get added into the other exercise which will target that muscle group

        if self.workout_type != "Balanced":
            if self.workout_type == "Focus on legs" and self.physical_activity == "low":
                legs_exercise = None
                # x and y are stopping conditions for every for loop
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        legs_exercise = exercise[0]
                        y += 1
                self.push_day3[2] = legs_exercise
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:                                              #makes sure that different exercises get added
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and legs_exercise != exercise[0]:
                        legs_exercise = exercise[0]
                        y += 1
                self.pull_day3[2] = legs_exercise
                
            elif self.workout_type == "Focus on legs" and self.physical_activity == "moderate":
                legs_exercise = None
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        legs_exercise = exercise[0]
                        y += 1
                self.push_day3[3] = legs_exercise
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and legs_exercise != exercise[0]:
                        legs_exercise = exercise[0]
                        y += 1
                self.pull_day3[3] = legs_exercise

            elif self.workout_type == "Focus on legs" and self.physical_activity == "vigorous":
                legs_exercise = None
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        legs_exercise = exercise[0]
                        y += 1
                self.push_day3[4] = legs_exercise
                x = 1
                y = 0
                for exercise in self.lower_body_exercises:
                    if "legs" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and legs_exercise != exercise[0]:
                        legs_exercise = exercise[0]
                        y += 1
                self.pull_day3[4] = legs_exercise

            elif self.workout_type == "Focus on back" and self.physical_activity == "low":
                back_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        back_exercise = exercise[0]
                        y += 1
                self.push_day3[2] = back_exercise
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and back_exercise != exercise[0]:
                        back_exercise = exercise[0]
                        y += 1
                self.legs_day3[2] = back_exercise

            elif self.workout_type == "Focus on back" and self.physical_activity == "moderate":
                back_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        back_exercise = exercise[0]
                        y += 1
                self.push_day3[3] = back_exercise
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and back_exercise != exercise[0]:
                        back_exercise = exercise[0]
                        y += 1
                self.legs_day3[3] = back_exercise

            elif self.workout_type == "Focus on back" and self.physical_activity == "vigorous":
                back_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        back_exercise = exercise[0]
                        y += 1
                self.push_day3[4] = back_exercise
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "back" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and back_exercise != exercise[0]:
                        back_exercise = exercise[0]
                        y += 1
                self.legs_day3[4] = back_exercise

            elif self.workout_type == "Focus on biceps" and self.physical_activity == "low":
                biceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        biceps_exercise = exercise[0]
                        y += 1
                self.push_day3[2] = biceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and biceps_exercise != exercise[0]:
                        biceps_exercise = exercise[0]
                        y += 1
                self.legs_day3[2] = biceps_exercise

            elif self.workout_type == "Focus on biceps" and self.physical_activity == "moderate":
                biceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        biceps_exercise = exercise[0]
                        y += 1
                self.push_day3[3] = biceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and biceps_exercise != exercise[0]:
                        biceps_exercise = exercise[0]
                        y += 1
                self.legs_day3[3] = biceps_exercise

            elif self.workout_type == "Focus on biceps" and self.physical_activity == "vigorous":
                biceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        biceps_exercise = exercise[0]
                        y += 1
                self.push_day3[4] = biceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "biceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and biceps_exercise != exercise[0]:
                        biceps_exercise = exercise[0]
                        y += 1
                self.legs_day3[4] = biceps_exercise

            elif self.workout_type == "Focus on triceps" and self.physical_activity == "low":
                triceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        triceps_exercise = exercise[0]
                        y += 1
                self.pull_day3[2] = triceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and triceps_exercise != exercise[0]:
                        triceps_exercise = exercise[0]
                        y += 1
                self.legs_day3[2] = triceps_exercise

                if None in self.pull_day3:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                            triceps_exercise = exercise[0]
                            y += 1
                    self.pull_day3[2] = triceps_exercise

                if None in self.legs_day3:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and exercise[0] != triceps_exercise:
                            triceps_exercise = exercise[0]
                            y += 1
                    self.legs_day3[2] = triceps_exercise


            elif self.workout_type == "Focus on triceps" and self.physical_activity == "moderate":
                triceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        triceps_exercise = exercise[0]
                        y += 1
                self.pull_day3[3] = triceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and triceps_exercise != exercise[0]:
                        triceps_exercise = exercise[0]
                        y += 1
                self.legs_day3[3] = triceps_exercise

                if None in self.pull_day3:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                            triceps_exercise = exercise[0]
                            y += 1
                    self.pull_day3[3] = triceps_exercise

                if None in self.legs_day3:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and exercise[0] != triceps_exercise:
                            triceps_exercise = exercise[0]
                            y += 1
                self.legs_day3[3] = triceps_exercise

            elif self.workout_type == "Focus on triceps" and self.physical_activity == "vigorous":
                triceps_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        triceps_exercise = exercise[0]
                        y += 1
                self.pull_day3[4] = triceps_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and triceps_exercise != exercise[0]:
                        triceps_exercise = exercise[0]
                        y += 1
                self.legs_day3[4] = triceps_exercise

                if None in self.pull_day3:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                            triceps_exercise = exercise[0]
                            y += 1
                    self.pull_day3[4] = triceps_exercise
                    
                if None in self.legs_day3:
                    x = 1
                    y = 0
                    for exercise in self.compound_exercises:
                        if "triceps" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and exercise[0] != triceps_exercise:
                            triceps_exercise = exercise[0]
                            y += 1
                self.legs_day3[4] = triceps_exercise

            elif self.workout_type == "Focus on shoulders" and self.physical_activity == "low":
                shoulders_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.pull_day3[2] = shoulders_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and shoulders_exercise != exercise[0]:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.legs_day3[2] = shoulders_exercise

            elif self.workout_type == "Focus on shoulders" and self.physical_activity == "moderate":
                shoulders_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.pull_day3[3] = shoulders_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and shoulders_exercise != exercise[0]:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.legs_day3[3] = shoulders_exercise

            elif self.workout_type == "Focus on shoulders" and self.physical_activity == "vigorous":
                shoulders_exercise = None
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.pull_day3[4] = shoulders_exercise
                x = 1
                y = 0
                for exercise in self.upper_body_exercises:
                    if "shoulders" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and shoulders_exercise != exercise[0]:
                        shoulders_exercise = exercise[0]
                        y += 1
                self.legs_day3[4] = shoulders_exercise

            elif self.workout_type == "Focus on chest" and self.physical_activity == "low":
                chest_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        chest_exercise = exercise[0]
                        y += 1
                self.pull_day3[2] = chest_exercise
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and chest_exercise != exercise[0]:
                        chest_exercise = exercise[0]
                        y += 1
                self.legs_day3[2] = chest_exercise

            elif self.workout_type == "Focus on chest" and self.physical_activity == "moderate":
                chest_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        chest_exercise = exercise[0]
                        y += 1
                self.pull_day3[3] = chest_exercise
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and chest_exercise != exercise[0]:
                        chest_exercise = exercise[0]
                        y += 1
                self.legs_day3[3] = chest_exercise

            elif self.workout_type == "Focus on chest" and self.physical_activity == "vigorous":
                chest_exercise = None
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x:
                        chest_exercise = exercise[0]
                        y += 1
                self.pull_day3[4] = chest_exercise
                x = 1
                y = 0
                for exercise in self.compound_exercises:
                    if "chest" in exercise[2] and (exercise[3] == 1 or exercise[3]==None) and y < x and chest_exercise != exercise[0]:
                        chest_exercise = exercise[0]
                        y += 1
                self.legs_day3[4] = chest_exercise
            
            elif self.workout_type == "Focus on cardio" and self.physical_activity == "low":
                cardio_exercise = None
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x:
                        cardio_exercise = exercise[0]
                        y += 1
                self.pull_day3[2] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.legs_day3[2] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.push_day3[2] = cardio_exercise

            elif self.workout_type == "Focus on cardio" and self.physical_activity == "moderate":
                cardio_exercise = None
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x:
                        cardio_exercise = exercise[0]
                        y += 1
                self.pull_day3[3] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.legs_day3[3] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.push_day3[3] = cardio_exercise

            elif self.workout_type == "Focus on cardio" and self.physical_activity == "vigorous":
                cardio_exercise = None
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x:
                        cardio_exercise = exercise[0]
                        y += 1
                self.pull_day3[4] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.legs_day3[4] = cardio_exercise
                x = 1
                y = 0
                for exercise in self.cardio_exercises:
                    if (exercise[1] == 1 or exercise[1]==None) and y < x and cardio_exercise != exercise[0]:
                        cardio_exercise = exercise[0]
                        y += 1
                self.push_day3[4] = cardio_exercise
        #workout plan doesn't get changed if user wants a balanced workout
        else:
            pass

        self.insert_information()

    #method will insert the exercises into the correct fields in the workout_plan_details_table
    def insert_information(self):
        if self.physical_activity == "low" and self.current_weight > self.weight_goal:

            #get exercises
            push_ex_1 = self.push_day1[0]
            push_ex_2 = self.push_day1[1]
            push_ex_3 = self.push_day1[2]
            push_ex_4 = self.push_day1[3]
            pull_ex_1 = self.pull_day1[0]
            pull_ex_2 = self.pull_day1[1]
            pull_ex_3 = self.pull_day1[2]
            pull_ex_4 = self.pull_day1[3]
            legs_ex_1 = self.legs_day1[0]
            legs_ex_2 = self.legs_day1[1]
            legs_ex_3 = self.legs_day1[2]
            legs_ex_4 = self.legs_day1[3]
        
            conn = sqlite3.connect("information.db")
            cur = conn.cursor()
            #insert exercises
            cur.execute("""INSERT INTO workout_plan_details (id, user_fk, push_ex_1, push_ex_2, push_ex_3, push_ex_4, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.plan_key, self.account_key, push_ex_1, push_ex_2, push_ex_3, push_ex_4, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4))
            conn.commit()
            conn.close()
            self.display_plan()

        elif self.physical_activity == "low" and self.current_weight < self.weight_goal:

            #get exercises
            push_ex_1 = self.push_day2[0]
            push_ex_2 = self.push_day2[1]
            push_ex_3 = self.push_day2[2]
            push_ex_4 = self.push_day2[3]
            pull_ex_1 = self.pull_day2[0]
            pull_ex_2 = self.pull_day2[1]
            pull_ex_3 = self.pull_day2[2]
            pull_ex_4 = self.pull_day2[3]
            legs_ex_1 = self.legs_day2[0]
            legs_ex_2 = self.legs_day2[1]
            legs_ex_3 = self.legs_day2[2]
            legs_ex_4 = self.legs_day2[3]
        
            conn = sqlite3.connect("information.db")
            cur = conn.cursor()
            #insert exercises
            cur.execute("""INSERT INTO workout_plan_details (id, user_fk, push_ex_1, push_ex_2, push_ex_3, push_ex_4, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.plan_key, self.account_key, push_ex_1, push_ex_2, push_ex_3, push_ex_4, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4))
            conn.commit()
            conn.close()
            self.display_plan()

        elif self.physical_activity == "low" and self.current_weight == self.weight_goal:

            #get exercises
            push_ex_1 = self.push_day3[0]
            push_ex_2 = self.push_day3[1]
            push_ex_3 = self.push_day3[2]
            push_ex_4 = self.push_day3[3]
            pull_ex_1 = self.pull_day3[0]
            pull_ex_2 = self.pull_day3[1]
            pull_ex_3 = self.pull_day3[2]
            pull_ex_4 = self.pull_day3[3]
            legs_ex_1 = self.legs_day3[0]
            legs_ex_2 = self.legs_day3[1]
            legs_ex_3 = self.legs_day3[2]
            legs_ex_4 = self.legs_day3[3]

            conn = sqlite3.connect("information.db")
            cur = conn.cursor()
            #insert exercises
            cur.execute("""INSERT INTO workout_plan_details (id, user_fk, push_ex_1, push_ex_2, push_ex_3, push_ex_4, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.plan_key, self.account_key, push_ex_1, push_ex_2, push_ex_3, push_ex_4, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4))
            conn.commit()
            conn.close()
            self.display_plan()

        elif self.physical_activity == "moderate" and self.current_weight > self.weight_goal:

            #get exercises
            push_ex_1 = self.push_day1[0]
            push_ex_2 = self.push_day1[1]
            push_ex_3 = self.push_day1[2]
            push_ex_4 = self.push_day1[3]
            push_ex_5 = self.push_day1[4]
            pull_ex_1 = self.pull_day1[0]
            pull_ex_2 = self.pull_day1[1]
            pull_ex_3 = self.pull_day1[2]
            pull_ex_4 = self.pull_day1[3]
            pull_ex_5 = self.pull_day1[4]
            legs_ex_1 = self.legs_day1[0]
            legs_ex_2 = self.legs_day1[1]
            legs_ex_3 = self.legs_day1[2]
            legs_ex_4 = self.legs_day1[3]
            legs_ex_5 = self.legs_day1[4]
        
            conn = sqlite3.connect("information.db")
            cur = conn.cursor()
            #insert exercises
            cur.execute("""INSERT INTO workout_plan_details (id, user_fk, push_ex_1, push_ex_2, push_ex_3, push_ex_4, push_ex_5, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, pull_ex_5, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4, legs_ex_5) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.plan_key, self.account_key, push_ex_1, push_ex_2, push_ex_3, push_ex_4, push_ex_5, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, pull_ex_5, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4, legs_ex_5))
            conn.commit()
            conn.close()
            self.display_plan()

        elif self.physical_activity == "moderate" and self.current_weight < self.weight_goal:

            #get exercises
            push_ex_1 = self.push_day2[0]
            push_ex_2 = self.push_day2[1]
            push_ex_3 = self.push_day2[2]
            push_ex_4 = self.push_day2[3]
            push_ex_5 = self.push_day2[4]
            pull_ex_1 = self.pull_day2[0]
            pull_ex_2 = self.pull_day2[1]
            pull_ex_3 = self.pull_day2[2]
            pull_ex_4 = self.pull_day2[3]
            pull_ex_5 = self.pull_day2[4]
            legs_ex_1 = self.legs_day2[0]
            legs_ex_2 = self.legs_day2[1]
            legs_ex_3 = self.legs_day2[2]
            legs_ex_4 = self.legs_day2[3]
            legs_ex_5 = self.legs_day2[4]
        
            conn = sqlite3.connect("information.db")
            cur = conn.cursor()
            #insert exercises
            cur.execute("""INSERT INTO workout_plan_details (id, user_fk, push_ex_1, push_ex_2, push_ex_3, push_ex_4, push_ex_5, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, pull_ex_5, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4, legs_ex_5 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.plan_key, self.account_key, push_ex_1, push_ex_2, push_ex_3, push_ex_4, push_ex_5, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, pull_ex_5, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4, legs_ex_5))
            conn.commit()
            conn.close()
            self.display_plan()

        elif self.physical_activity == "moderate" and self.current_weight == self.weight_goal:

            #get exercises
            push_ex_1 = self.push_day3[0]
            push_ex_2 = self.push_day3[1]
            push_ex_3 = self.push_day3[2]
            push_ex_4 = self.push_day3[3]
            push_ex_5 = self.push_day3[4]
            pull_ex_1 = self.pull_day3[0]
            pull_ex_2 = self.pull_day3[1]
            pull_ex_3 = self.pull_day3[2]
            pull_ex_4 = self.pull_day3[3]
            pull_ex_5 = self.pull_day3[4]
            legs_ex_1 = self.legs_day3[0]
            legs_ex_2 = self.legs_day3[1]
            legs_ex_3 = self.legs_day3[2]
            legs_ex_4 = self.legs_day3[3]
            legs_ex_5 = self.legs_day3[4]
           
            conn = sqlite3.connect("information.db")
            cur = conn.cursor()
            #insert exercises
            cur.execute("""INSERT INTO workout_plan_details (id, user_fk, push_ex_1, push_ex_2, push_ex_3, push_ex_4, push_ex_5, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, pull_ex_5, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4, legs_ex_5) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? , ?, ?)""", (self.plan_key, self.account_key, push_ex_1, push_ex_2, push_ex_3, push_ex_4, push_ex_5, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, pull_ex_5, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4, legs_ex_5))
            conn.commit()
            conn.close()
            self.display_plan()

        elif self.physical_activity == "vigorous" and self.current_weight > self.weight_goal:

            #get exercises
            push_ex_1 = self.push_day1[0]
            push_ex_2 = self.push_day1[1]
            push_ex_3 = self.push_day1[2]
            push_ex_4 = self.push_day1[3]
            push_ex_5 = self.push_day1[4]
            push_ex_6 = self.push_day1[5]
            pull_ex_1 = self.pull_day1[0]
            pull_ex_2 = self.pull_day1[1]
            pull_ex_3 = self.pull_day1[2]
            pull_ex_4 = self.pull_day1[3]
            pull_ex_5 = self.pull_day1[4]
            pull_ex_6 = self.pull_day1[5]
            legs_ex_1 = self.legs_day1[0]
            legs_ex_2 = self.legs_day1[1]
            legs_ex_3 = self.legs_day1[2]
            legs_ex_4 = self.legs_day1[3]
            legs_ex_5 = self.legs_day1[4]
            legs_ex_6 = self.legs_day1[5]
        
            conn = sqlite3.connect("information.db")
            cur = conn.cursor()
            #insert exercises
            cur.execute("""INSERT INTO workout_plan_details (id, user_fk, push_ex_1, push_ex_2, push_ex_3, push_ex_4, push_ex_5, push_ex_6, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, pull_ex_5, pull_ex_6, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4, legs_ex_5, legs_ex_6 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.plan_key, self.account_key, push_ex_1, push_ex_2, push_ex_3, push_ex_4, push_ex_5, push_ex_6, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, pull_ex_5, pull_ex_6, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4, legs_ex_5, legs_ex_6))
            conn.commit()
            conn.close()
            self.display_plan()

        elif self.physical_activity == "vigorous" and self.current_weight < self.weight_goal:

            #get exercises
            push_ex_1 = self.push_day2[0]
            push_ex_2 = self.push_day2[1]
            push_ex_3 = self.push_day2[2]
            push_ex_4 = self.push_day2[3]
            push_ex_5 = self.push_day2[4]
            push_ex_6 = self.push_day2[5]
            pull_ex_1 = self.pull_day2[0]
            pull_ex_2 = self.pull_day2[1]
            pull_ex_3 = self.pull_day2[2]
            pull_ex_4 = self.pull_day2[3]
            pull_ex_5 = self.pull_day2[4]
            pull_ex_6 = self.pull_day2[5]
            legs_ex_1 = self.legs_day2[0]
            legs_ex_2 = self.legs_day2[1]
            legs_ex_3 = self.legs_day2[2]
            legs_ex_4 = self.legs_day2[3]
            legs_ex_5 = self.legs_day2[4]
            legs_ex_6 = self.legs_day2[5]
        
            conn = sqlite3.connect("information.db")
            cur = conn.cursor()
            #insert exercises
            cur.execute("""INSERT INTO workout_plan_details (id, user_fk, push_ex_1, push_ex_2, push_ex_3, push_ex_4, push_ex_5, push_ex_6, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, pull_ex_5, pull_ex_6, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4, legs_ex_5, legs_ex_6) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.plan_key, self.account_key, push_ex_1, push_ex_2, push_ex_3, push_ex_4, push_ex_5, push_ex_6, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, pull_ex_5, pull_ex_6, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4, legs_ex_5, legs_ex_6))
            conn.commit()
            conn.close()
            self.display_plan()

        elif self.physical_activity == "vigorous" and self.current_weight == self.weight_goal:

            #get exercises
            push_ex_1 = self.push_day3[0]
            push_ex_2 = self.push_day3[1]
            push_ex_3 = self.push_day3[2]
            push_ex_4 = self.push_day3[3]
            push_ex_5 = self.push_day3[4]
            push_ex_6 = self.push_day3[5]
            pull_ex_1 = self.pull_day3[0]
            pull_ex_2 = self.pull_day3[1]
            pull_ex_3 = self.pull_day3[2]
            pull_ex_4 = self.pull_day3[3]
            pull_ex_5 = self.pull_day3[4]
            pull_ex_6 = self.pull_day3[5]
            legs_ex_1 = self.legs_day3[0]
            legs_ex_2 = self.legs_day3[1]
            legs_ex_3 = self.legs_day3[2]
            legs_ex_4 = self.legs_day3[3]
            legs_ex_5 = self.legs_day3[4]
            legs_ex_6 = self.legs_day3[5]

            conn = sqlite3.connect("information.db")
            cur = conn.cursor()
            #insert exercises
            cur.execute("""INSERT INTO workout_plan_details (id, user_fk, push_ex_1, push_ex_2, push_ex_3, push_ex_4, push_ex_5, push_ex_6, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, pull_ex_5, pull_ex_6, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4, legs_ex_5, legs_ex_6 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? , ?, ?, ?, ?, ?)""", (self.plan_key, self.account_key, push_ex_1, push_ex_2, push_ex_3, push_ex_4, push_ex_5, push_ex_6, pull_ex_1, pull_ex_2, pull_ex_3, pull_ex_4, pull_ex_5, pull_ex_6, legs_ex_1, legs_ex_2, legs_ex_3, legs_ex_4, legs_ex_5, legs_ex_6))
            conn.commit()
            conn.close()
            self.display_plan()

    #method will write the user plan key to the text file, then go to display_plan
    def display_plan(self):
        with open("Scripts/user_plan_key.txt","w") as file:
            file.write(str(self.plan_key))
        script_path = os.path.join("Scripts", "display_plan.py")
        subprocess.run(["python", script_path])
        self.close_everything()   

    #This method will delete all user's personal information and return back to homepage
    def discard(self):
        conn = sqlite3.connect("information.db")
        cur = conn.cursor()
        #deletes most recent entry
        cur.execute("DELETE FROM user_personal_info WHERE main_id = (SELECT MAX(main_id) FROM user_personal_info)")
        cur.execute("DELETE FROM equipment_access WHERE main_id = (SELECT MAX(main_id) FROM equipment_access)")
        cur.execute("DELETE FROM workout_plan_details WHERE main_id = (SELECT MAX(main_id) FROM workout_plan_details)")
        conn.commit()
        conn.close()
        script_path = os.path.join("Scripts", "homepage.py")
        subprocess.run(["python", script_path])
        self.close_everything()

    #This method will delete all user's personal information if window is closed by user
    def discard_on_close(self):
        conn = sqlite3.connect("information.db")
        cur = conn.cursor()
        #deletes most recent entry
        cur.execute("DELETE FROM user_personal_info WHERE main_id = (SELECT MAX(main_id) FROM user_personal_info)")
        cur.execute("DELETE FROM equipment_access WHERE main_id = (SELECT MAX(main_id) FROM equipment_access)")
        cur.execute("DELETE FROM workout_plan_details WHERE main_id = (SELECT MAX(main_id) FROM workout_plan_details)")
        conn.commit()
        conn.close()
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



#note that script paths may need to be adjusted to user's directories/file system

#import hashing and sql libraries
#This video was used for understanding hashing in python https://www.youtube.com/watch?v=i-h0CtKde6w&t=575s
import hashlib
import sqlite3

#import regular expressions to check if password has at least one capital letter and at least one special character
#this module was learned from from https://www.youtube.com/watch?v=Dkiz0z3bMg0
import re

#call and subprocess was learned from https://www.youtube.com/watch?v=CUFIjz_U7Mo
#and https://www.youtube.com/watch?v=2Fp1N6dof0Y respectively
#These videos gave me understanding of os.path.join and __file__ (to get current folder path) respectively: https://www.youtube.com/watch?v=tJxcKyFMTGo, https://www.youtube.com/watch?v=LVhxqOznPg0
#import library to switch between files
from subprocess import call
import subprocess
#import os to access directories
import os
#import gui libraries, fundamentals of tkinter was learned from https://www.youtube.com/watch?v=ibf5cx221hk&t=1367s
#and i used customtkinter documentation: https://customtkinter.tomschimansky.com/documentation/
import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
from tkinter import font

#I used https://www.youtube.com/watch?v=eaxPK9VIkFM to learn how to use classes with customtkinter, and this documentation: https://github.com/TomSchimansky/CustomTkinter/wiki/CTk-(tkinter.Tk)
#I did not understand superclasses so I used this video for understanding: https://www.youtube.com/watch?v=RSl87lqOXDE
#I learned **kwargs (keywordarguments) from https://www.youtube.com/watch?v=GdSJAZDsCZA, to optimise my code with classes in customtkinter

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
class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        #set title, window size and make it so the user cannot change the size of window
        self.title("FitPro")
        self.geometry("790x450")
        self.resizable(False, False)

        #Create fonts
        self.title_font = Font("Helvetica", 20, "bold")
        self.header_font = Font(family="Helvetica", size = 18,weight="bold")
        self.small_font = Font("Helvetica", 10,"bold")

        #use "register" and "delete account" entries as variables for registerinfo and delete_account functions
        self.username = StringVar()
        self.password = StringVar()
        self.confirm_password_input = StringVar()

        #use "login" entries as variables for login function
        self.username_by_user = StringVar()
        self.password_by_user = StringVar()
        
        #method called when user wants to close the window
        self.protocol("WM_DELETE_WINDOW", self.close_everything)

        #create and place widgets
        self.login_label = Label(self, "Login", x=170, y=50, font=self.title_font)
        self.username_label = Label(self, "Username", x=70, y=100, font=self.header_font)
        self.username_entry = Entry(self, "", self.username_by_user, x=170, y=100)
        self.password_entry = Entry(self, "*", self.password_by_user, x=170, y=160)
        self.password_label = Label(self, "Password", x=70, y=160, font=self.header_font)
        self.login_button = Button(self, "Login", self.login, x=170, y=210)
        self.delete_button = Button(self, "Delete", self.delete_accountbutton, x=170, y=305)
        self.deleteaccount_label = Label(self, "Delete Account?", x=170, y=265, font=self.header_font)
        self.register_label = Label(self, "Register", x=590, y=50, font=self.title_font)
        self.newusername_label = Label(self, "New Username", x=450, y=100, font=self.header_font)
        self.newusername_entry = Entry(self, "", self.username, x=590, y=100)
        self.newpassword_entry = Entry(self, "*", self.password, x=590, y=160)
        self.newpassword_label = Label(self, "New Password", x=450, y=160, font=self.header_font)
        self.register_button = Button(self, "Register", self.getinfo_register, x=590, y=270)
        self.confirm_password_label = Label(self, "Confirm Password", x=415, y=220, font=self.header_font)
        self.confirm_password_entry = Entry(self, "*", self.confirm_password_input, x=590, y=220)
        self.credentialslengths_label = Label(self, "1. Password must be at least 5 characters long, username\n and password must be under 15 characters in length", x=450, y=320, font=self.small_font)
        self.passwordrequirements_label = Label(self, "2. Password must have at least one capital letter\n and special character", x=450, y=360, font=self.small_font)
        self.notidentical_label = Label(self, "3. New password must be identical to confirm password", x=450, y=390, font=self.small_font)
        self.change_details_button = Button(self, "Change Account\nDetails", self.change_account_details, x=170, y=390)
        self.change_details_label = Label(self, "Forgot Details?", font=self.header_font, x=170,y=350)
        #create database when window starts running
        self.create_database()

    #add username and hashed password to database if they match requirements
    def getinfo_register(self):
        #get all values from entry boxes and get the lengths of the user's inputs
        self.username_info = self.username.get()
        self.password_info = self.password.get()
        self.confirm_password = self.confirm_password_input.get()
        self.usernamelength = len(self.username_info)
        self.passwordlength = len(self.password_info)
        #go to next check
        self.check_lengths()

    def check_lengths(self):
        #checks if inputs are empty or not
        if self.username_info != "":
            if self.password_info != "":
                #checks if new username and new password is too long
                if self.usernamelength < 15:
                    if self.passwordlength < 15:
                        #checks if password is too short
                        if self.passwordlength >= 5:
                            #go to next check
                            self.check_identical()
                        #error message will appear if any requirements are not met
                        else:
                            messagebox.showerror(title="Error",message="Password must be at least 5 characters long")
                            self.newpassword_entry.delete(0, END)
                            self.confirm_password_entry.delete(0,END)
                    else:
                        messagebox.showerror("error", message="Password is too long")
                        self.newpassword_entry.delete(0, END)
                        self.confirm_password_entry.delete(0,END)
                else:
                    messagebox.showerror("error", message="Username is too long") 
                    self.newusername_entry.delete(0, END)
                    self.newpassword_entry.delete(0, END)
                    self.confirm_password_entry.delete(0,END) 
            else:
                messagebox.showerror(title="Error", message="Password cannot be empty")
                self.newpassword_entry.delete(0, END)
                self.confirm_password_entry.delete(0,END)  
        else:
            messagebox.showerror(title="Error", message="Username cannot be empty") 
            self.newpassword_entry.delete(0, END)
            self.confirm_password_entry.delete(0,END)                   

    def check_identical(self):
        #check if confirm password and new password match
        if self.password_info == self.confirm_password:
            #go to next check
            self.special_and_capital()
        #error message will appear if requirement is not met
        else:
            messagebox.showerror(title="error",message="Passwords must be identical")
            self.newpassword_entry.delete(0, END)
            self.confirm_password_entry.delete(0,END)
        
    def special_and_capital(self):
        #check if there is at least one capital letter and special character in new password, 
        #the "\" allows the character after it to be accepted as a character
        if (re.search(r'[\\!@#$%()?^&*()_\-+={}[\]|\/:;"\'<>,.]', self.password_info)):
            if (re.search(r'[A-Z]', self.password_info)):
                self.register_info()
        #error message will appear if any requirements are not met
            else:
                messagebox.showerror(title="Error", message="Password must contain at least one capital letter")
                self.newpassword_entry.delete(0, END)
                self.confirm_password_entry.delete(0,END)
        else:
            messagebox.showerror(title="Error", message="Password must contain at least one special character")
            self.newpassword_entry.delete(0, END)
            self.confirm_password_entry.delete(0,END)

    def register_info(self):
        #automatically makes new username lowercase for better accessibility
        username_info = self.username_info.lower()
        #hashes new password for security
        h = hashlib.sha256()
        h.update(self.password_info.encode("utf-8"))
        #exception handling used so users cannot make multiple accounts with the same username
        try:
            hashed_password = h.hexdigest()
            #new username and hashed new password will get added to the database, and user will login automatically
            conn = sqlite3.connect("information.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (username_info, hashed_password))
            conn.commit()
            cur.execute("SELECT id FROM users WHERE username=?", (username_info,))
            #get primary key value so foreign key can be used in database
            primary_key_line = cur.fetchone()
            primary_key = primary_key_line[0]
            conn.close()
            #write the primary key value to text file so it can be fetched from the text file as a foreign key
            #get folder path all the way to current folder
            current_folder = os.path.dirname(__file__)
            #add subfolder to the folder path
            scripts_folder_path = os.path.join(current_folder, "Scripts")
            #then join path with file needed
            file_path = os.path.join(scripts_folder_path, "user_account_key.txt")
            #write the user's account key to text file for access to information, by using the folder path created
            with open(file_path,"w") as file:
                    file.write(str(primary_key))
            messagebox.showinfo(title="Success", message="Account has been created")
            self.enter()
        #if user with same username already exists in database, error message will appear
        except sqlite3.IntegrityError:
            #close connection here so database does not lock out
            conn.close()
            messagebox.showerror(title="Error", message="User already exists")
            self.newpassword_entry.delete(0, END)
            self.confirm_password_entry.delete(0,END)

    #goes to homepage if credentials are correct
    def login_correct(self):
        messagebox.showinfo(title="Login Success", message="You successfully logged in")
        #access file subfolder by joining the Scripts with homepage.py file, so that "Scripts\homepage.py can be called"
        script_path = os.path.join("Scripts", "homepage.py")
        call(["python", script_path])
        self.close_everything()

    #go to homepage after successful registration
    def enter(self):
        script_path = os.path.join("Scripts", "homepage.py")
        call(["python",script_path])
        self.close_everything()

    #compare user input with username and hashed password database
    def login(self):
        username1 = self.username_by_user.get()
        password1 = self.password_by_user.get()
        username1 = username1.lower()
        h = hashlib.sha256()
        h.update(password1.encode("utf-8"))
        input_password = h.hexdigest() 
        conn = sqlite3.connect("information.db")
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username=?", (username1,))
        data = cur.fetchone()
        cur.execute("SELECT id FROM users WHERE username=?", (username1,))
        #get primary key value so foreign key can be used in database
        primary_key_line = cur.fetchone()
        conn.close()
            
        #checks if account(username) exists, then checks if password matches
        if data is not None:
            if input_password == data[0]:
                #write the primary key value to text file so it can be fetched from the text file as a foreign key
                current_folder = os.path.dirname(__file__)
                scripts_folder_path = os.path.join(current_folder, "Scripts")
                file_path = os.path.join(scripts_folder_path, "user_account_key.txt")

                primary_key = primary_key_line[0]
                with open(file_path,"w") as file:
                    file.write(str(primary_key))
                self.login_correct()
            else:
                messagebox.showerror(title="Error", message="Invalid password")
                self.password_entry.delete(0,END)
        else:
            messagebox.showerror(title="Error", message="User has not been found")
            self.password_entry.delete(0,END)

    #go to "deleteaccount" page
    def delete_accountbutton(self):
        script_path = os.path.join("Scripts", "delete_account.py")
        call(["python",script_path])
        self.close_everything()

    #go to "change_details" page
    def change_account_details(self):
        script_path = os.path.join("Scripts", "change_details.py")
        call(["python",script_path])
        self.close_everything()
        
    #create database for user, so app can be used                                  
    def create_database(self):
        script_path = os.path.join("Scripts", "create_database.py")
        #check if database already exists
        if os.path.isfile("information.db"):
            #if database already exists, nothing will happen
            pass
        else:
            try:
                subprocess.run(["python", script_path])
            except Exception as e:
                messagebox.showerror(title = "Error",message =  f"Error creating the database: {str(e)}")  

    #method to delete every widget before closing window
    def close_everything(self):
        children = self.winfo_children()
        for widget in children:
            widget.destroy()
        self.quit()

#run window
if __name__ == "__main__":
    app = Window()
    app.mainloop()
    
    
 

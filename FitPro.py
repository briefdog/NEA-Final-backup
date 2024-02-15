#import hashing and sql libraries
import hashlib
import sqlite3

#import regular expressions to check if password has at least one capital letter and at least one special character
#this module was learned from from https://www.youtube.com/watch?v=Dkiz0z3bMg0
import re

#call and subprocess was learned from https://www.youtube.com/watch?v=CUFIjz_U7Mo
#and https://www.youtube.com/watch?v=2Fp1N6dof0Y respectively
#import library to switch between files
from subprocess import call
import os
import subprocess
#import gui libraries, fundamentals of tkinter was learned from https://www.youtube.com/watch?v=ibf5cx221hk&t=1367s
#and i used customtkinter documentation: https://customtkinter.tomschimansky.com/documentation/
import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
from tkinter import font

#I used https://www.youtube.com/watch?v=eaxPK9VIkFM to learn how to use classes with tkinter
#I learned **kwargs (keywordarguments) from https://www.youtube.com/watch?v=GdSJAZDsCZA

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
        self.geometry("790x440")
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

        #create and place widgets for login
        self.login_label = Label(self, "Login", x=170, y=50, font=self.title_font)
        self.username_label = Label(self, "Username", x=70, y=100, font=self.header_font)
        self.username_entry = Entry(self, "", self.username_by_user, x=170, y=100)
        self.password_entry = Entry(self, "*", self.password_by_user, x=170, y=160)
        self.password_label = Label(self, "Password", x=70, y=160, font=self.header_font)
        self.login_button = Button(self, "Login", self.login, x=170, y=210)
        self.delete_button = Button(self, "Delete", self.delete_accountbutton, x=170, y=305)
        self.deleteaccount_label = Label(self, "Delete Account?", x=170, y=265, font=self.header_font)
        self.database_label = Label(self, "(Make sure that the database is installed\nor else the app will not work)", x=150, y=360, font=self.small_font)
        self.createdatabase_button = Button(self, "Create database", self.create_database, x=170, y=390)

        #create and place widgets for register
        self.register_label = Label(self, "Register", x=590, y=50, font=self.title_font)
        self.newusername_label = Label(self, "New Username", x=450, y=100, font=self.header_font)
        self.newusername_entry = Entry(self, "", self.username, x=590, y=100)
        self.newpassword_entry = Entry(self, "*", self.password, x=590, y=160)
        self.newpassword_label = Label(self, "New Password", x=450, y=160, font=self.header_font)
        self.register_button = Button(self, "Register", self.registerinfo, x=590, y=270)
        self.confirm_password_label = Label(self, "Confirm Password", x=410, y=220, font=self.header_font)
        self.confirm_password_entry = Entry(self, "*", self.confirm_password_input, x=590, y=220)
        self.credentialslengths_label = Label(self, "1. Password and username must be at least 5 characters long\n and under 15 characters in length", x=450, y=320, font=self.small_font)
        self.passwordrequirements_label = Label(self, "2. Password must have at least one capital letter\n and special character", x=450, y=360, font=self.small_font)
        self.notidentical_label = Label(self, "3. password and username must not be identical", x=450, y=390, font=self.small_font)

    #add username and hashed password to database if they match requirements
    def registerinfo(self):
        #get all values from entry boxes and get the lengths of the user's inputs
        username_info = self.username.get()
        password_info = self.password.get()
        confirm_password = self.confirm_password_input.get()
        usernamelength = len(username_info)
        passwordlength = len(password_info)
        #check if new username and new password entries are empty, and if database exists
        if os.path.isfile("information.db"):  
            if username_info != "":
                if password_info != "":
                    #checks if new username and new password is shorter than 15 characters
                    if usernamelength < 15:
                        if passwordlength < 15:   
                            #checks if new username and new password are identical
                            if username_info != password_info:
                                #checks if new username and new password is at least 5 characters
                                if usernamelength >= 5:
                                    if passwordlength >= 5:
                                        #automatically makes new username lowercase for better accessibility
                                        username_info = username_info.lower()
                                        #hashes new password for security
                                        h = hashlib.sha256()
                                        h.update(password_info.encode("utf-8"))
                                        #exception handling used so users cannot make multiple accounts with the same username
                                        try:
                                            hashed_password = h.hexdigest()
                                            #check if there is at least one capital letter and special character in new password
                                            if (re.search(r'[\\!@#$%^&*()_\-+={}[\]|\/:;"\'<>,.]', password_info)) and (re.search(r'[A-Z]', password_info)):
                                                #check if new password is identical to confirm pasword
                                                if password_info == confirm_password:
                                                    if os.path.isfile("information.db"):
                                                        #if all checks, are passed, new username and hashed new password will get added to the database, and user will login automatically
                                                        conn = sqlite3.connect("information.db")
                                                        cur = conn.cursor()
                                                        cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (username_info, hashed_password))
                                                        conn.commit()
                                                        cur.execute("SELECT id FROM users WHERE username=?", (username_info,))
                                                        #get primary key value so foreign key can be used in database
                                                        primary_key = cur.fetchone()
                                                        conn.close()
                                                        #write the primary key value to text file so it can be fetched from the text file as a foreign key
                                                        current_folder = os.path.dirname(__file__)
                                                        scripts_folder_path = os.path.join(current_folder, "Scripts")
                                                        file_path = os.path.join(scripts_folder_path, "user_account_key.txt")

                                                        with open(file_path,"w") as file:
                                                                file.write(str(primary_key))
                                                        messagebox.showinfo(title="Success", message="Account has been created")
                                                        self.enter()
                                                    else:
                                                        messagebox.showerror(title = "Error",message="Database does not exist")
                                                #an error message will pop up if any of the requirements are not satisfied
                                                else:
                                                    messagebox.showerror(title="error",message="Passwords must be identical")
                                                    self.newpassword_entry.delete(0, END)
                                                    self.confirm_password_entry.delete(0,END)
                                            else:
                                                messagebox.showerror(title="Error", message="Password must contain at least one capital letter and at least one special character")
                                                self.newpassword_entry.delete(0, END)
                                                self.confirm_password_entry.delete(0,END)
                                        except sqlite3.IntegrityError:
                                            messagebox.showerror(title="Error", message="User already exists")
                                            self.newpassword_entry.delete(0, END)
                                            self.confirm_password_entry.delete(0,END)
                                    else:
                                        messagebox.showerror(title="Error",message="Password must be at least 5 characters long")
                                        self.newpassword_entry.delete(0, END)
                                        self.confirm_password_entry.delete(0,END)
                                else:
                                    messagebox.showerror(title="Error", message="Username must be at least 5 characters long")
                                    self.newpassword_entry.delete(0, END)
                                    self.confirm_password_entry.delete(0,END)
                            else:
                                messagebox.showerror(title="Error", message="Username and password cannot be identical")
                                self.newpassword_entry.delete(0, END)
                                self.confirm_password_entry.delete(0,END)
                        else:
                            messagebox.showerror("error", message="Password is too long")
                            self.newpassword_entry.delete(0, END)
                            self.confirm_password_entry.delete(0,END)
                    else:
                        messagebox.showerror("error", message="Username is too long") 
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
        else:
            messagebox.showerror(title = "Error",message="Database does not exist")
            self.newpassword_entry.delete(0, END)
            self.confirm_password_entry.delete(0,END)
        

    #goes to homepage if credentials are correct
    def login_correct(self):
        messagebox.showinfo(title="Login Success", message="You successfully logged in")
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
        if os.path.isfile("information.db"):  
            conn = sqlite3.connect("information.db")
            cur = conn.cursor()
            cur.execute("SELECT password FROM users WHERE username=?", (username1,))
            data = cur.fetchone()
            cur.execute("SELECT id FROM users WHERE username=?", (username1,))
            #get primary key value so foreign key can be used in database
            primary_key = cur.fetchone()
            conn.close()
                
            #checks if account(username) exists, then checks if password matches
            if data is not None:
                if input_password == data[0]:
                    #write the primary key value to text file so it can be fetched from the text file as a foreign key
                    current_folder = os.path.dirname(__file__)
                    scripts_folder_path = os.path.join(current_folder, "Scripts")
                    file_path = os.path.join(scripts_folder_path, "user_account_key.txt")

                    with open(file_path,"w") as file:
                        file.write(str(primary_key))
                    self.login_correct()
                else:
                    messagebox.showerror(title="Error", message="Invalid password")
                    self.password_entry.delete(0,END)
            else:
                messagebox.showerror(title="Error", message="User has not been found")
                self.password_entry.delete(0,END)
        else:
            messagebox.showerror(title = "Error",message="Database does not exist")

    #go to "deleteaccount" page
    def delete_accountbutton(self):
        script_path = os.path.join("Scripts", "deleteaccount.py")
        call(["python",script_path])
        self.close_everything()
        
    #create database for user, so app can be used                                  
    def create_database(self):
        script_path = os.path.join("Scripts", "create_database.py")
        if os.path.isfile("information.db"):
            messagebox.showerror(title = "Error", message = "Database already exists")
        else:
            try:
                subprocess.run(["python", script_path])
                messagebox.showinfo(title = "Success", message = "Database created successfully")
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
    app = window()
    app.mainloop()

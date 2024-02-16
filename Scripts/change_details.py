#import libraries
import subprocess
from subprocess import call
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import os

#import hashing and sql libraries
import hashlib
import sqlite3
import re

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
        self.geometry("800x500")
        self.resizable(False, False)

        #collect entries as variables
        self.current_username1 = StringVar()
        self.current_password1 = StringVar()
        self.current_username2 = StringVar()
        self.current_password2 = StringVar()
        self.new_password = StringVar()
        self.confirm_new_password = StringVar()
        self.new_username = StringVar()
        self.confirm_new_username = StringVar()

        #create font
        self.main_title_font = Font("Helvetica", 25, "bold")
        self.title_font = Font("Helvetica", 22, "bold")
        self.header_font = Font("Helvetica", 18, "bold")

        #create and display widgets
        self.change_details_label = Label(self,"Change your\naccount details", self.main_title_font,x=350,y=5)
        self.return_button = Button(self, "Go back to\nlogin page", self.go_back,x=10,y=10)
        self.change_password_button = Button(self, "Change password", self.change_password,x=200,y=350)
        self.change_username_button = Button(self, "Change username", self.change_username,x=560,y=350)
        self.change_password_label = Label(self,"Change password", self.title_font, x=170,y=90)
        self.change_username_label = Label(self,"Change username", self.title_font,x=550,y=90)
        self.current_username_label1 = Label(self,"Current username", self.header_font,x=30,y=150)
        self.current_password_label1 = Label(self,"Current password", self.header_font,x=30,y=200)
        self.current_username_label2 = Label(self,"Current username", self.header_font,x=390,y=150)
        self.current_password_label2 = Label(self,"Current password", self.header_font,x=390,y=200)
        self.new_password_label = Label(self,"New password", self.header_font,x=30,y=250)
        self.new_username_label = Label(self,"New username", self.header_font,x=390,y=250)
        self.confirm_new_password_label = Label(self,"Confirm new\npassword", self.header_font,x=40,y=290)
        self.confirm_new_username_label = Label(self,"Confirm new\nusername", self.header_font,x=400,y=290)
        self.current_username_entry1 = Entry(self, "", self.current_username1,x=200,y=150)
        self.current_password_entry1 = Entry(self, "*", self.current_password1,x=200,y=200)
        self.current_username_entry2 = Entry(self, "", self.current_username2,x=560,y=150)
        self.current_password_entry2 = Entry(self, "*", self.current_password2,x=560,y=200)
        self.new_password_entry = Entry(self, "*", self.new_password,x=200,y=250)
        self.new_username_entry = Entry(self, "", self.new_username,x=560,y=250)
        self.confirm_new_password_entry = Entry(self, "*", self.confirm_new_password,x=200,y=300)
        self.confirm_new_username_entry = Entry(self, "", self.confirm_new_username,x=560,y=300)

    def change_password(self):
        current_username = self.current_username1.get()
        current_password = self.current_password1.get()
        new_password = self.new_password.get()
        confirm_new_password = self.confirm_new_password.get()
        #get length of new password
        new_password_length = len(new_password)
        current_username = current_username.lower()
        #hash current password and new password entries so that current password can be compared to the hashed password in the database,
        #and so the new password can be added into the database as a hashed string, for security
        h = hashlib.sha256()
        h.update(current_password.encode("utf-8"))
        hashed_current_password = h.hexdigest()
        h = hashlib.sha256()
        h.update(new_password.encode("utf-8"))
        hashed_new_password = h.hexdigest()
        #checks if database exists
        if os.path.isfile("information.db"):
            #checks if any entries are empty or not
            if current_username and current_password and new_password and confirm_new_password != "":
                #checks if current password matches confirm new password
                if new_password == confirm_new_password:
                    conn = sqlite3.connect("information.db")
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM users WHERE username=?",(current_username,))
                    user = cur.fetchone()
                    conn.close()
                    #checks if account with entered username exists
                    if user is not None:
                        correct_password = user[2]
                        #checks if current password matches with password in database
                        if correct_password == hashed_current_password:
                            #checks length of new password
                            if new_password_length < 15:
                                if new_password_length >= 5:
                                    #checks if there is at least one special character and at least one number in the new password
                                    if (re.search(r'[\\!@#$%^&*()_\-+={}[\]|\/:;"\'<>,.]', new_password)) and (re.search(r'[A-Z]', new_password)):
                                        #checks if the password needs to be changed
                                        if current_password != new_password:
                                            conn = sqlite3.connect("information.db")
                                            cur = conn.cursor()
                                            cur.execute("UPDATE users SET password=? WHERE username=?", (hashed_new_password, current_username))
                                            conn.commit()
                                            conn.close()
                                            messagebox.showinfo(title = "Success", message = "Password has been changed successfully")
                                            self.current_username_entry1.delete(0,END)
                                            self.current_password_entry1.delete(0,END)
                                            self.new_password_entry.delete(0,END)
                                            self.confirm_new_password_entry.delete(0,END) 
                                        #an error message will pop up if any of the requirements are not satisfied
                                        else:
                                            messagebox.showerror(title="Error", message="New password must not be identical to current password")
                                            self.new_password_entry.delete(0,END)
                                            self.confirm_new_password_entry.delete(0,END)
                                    else:
                                        messagebox.showerror(title="Error", message="New password must contain at least one capital letter and at least one special character")
                                        self.new_password_entry.delete(0,END)
                                        self.confirm_new_password_entry.delete(0,END)      
                                else:
                                    messagebox.showerror(title = "Error", message = "New password must be at least 5 characters long")
                                    self.new_password_entry.delete(0,END)
                                    self.confirm_new_password_entry.delete(0,END)
                            else:
                                messagebox.showerror(title = "Error", message = "New password is too long")
                                self.new_password_entry.delete(0,END)
                                self.confirm_new_password_entry.delete(0,END)
                        else:
                            messagebox.showerror(title = "Error", message = "Current password entered is incorrect")
                            self.new_password_entry.delete(0,END)
                            self.confirm_new_password_entry.delete(0,END)
                    else:
                        messagebox.showerror(title = "Error", message = "User not found")
                        self.new_password_entry.delete(0,END)
                        self.confirm_new_password_entry.delete(0,END)
                else:
                    messagebox.showerror(title= "Error",message = "New password must be identical to confirm new password")
                    self.new_password_entry.delete(0,END)
                    self.confirm_new_password_entry.delete(0,END)
            else:
                messagebox.showerror(title= "Error",message = "None of the entry boxes should be empty")
                self.new_password_entry.delete(0,END)
                self.confirm_new_password_entry.delete(0,END)
        else:
            messagebox.showerror(title = "Error",message="Database does not exist")
            self.new_password_entry.delete(0,END)
            self.confirm_new_password_entry.delete(0,END)

    def change_username(self):
        current_username = self.current_username2.get()
        current_password = self.current_password2.get()
        new_username= self.new_username.get()
        confirm_new_username = self.confirm_new_username.get()
        #get length of new username
        new_username_length = len(new_username)
        #hash current password entry so that it can be compared to the hashed password in the database
        h = hashlib.sha256()
        h.update(current_password.encode("utf-8"))
        hashed_current_password = h.hexdigest()
        #checks if database exists
        if os.path.isfile("information.db"):
            #checks if any entries are empty or not
            if current_username and current_password and new_username and confirm_new_username != "":
                #checks if current username matches confirm new username
                if new_username == confirm_new_username:
                    conn = sqlite3.connect("information.db")
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM users WHERE username=?",(current_username,))
                    user = cur.fetchone()
                    conn.close()
                    #checks if account with entered username exists
                    if user is not None:
                        #checks length of new username
                        if new_username_length < 15:
                            if new_username_length >= 5:
                                correct_password = user[2]
                                #checks if current password matches with password in database
                                if hashed_current_password == correct_password:
                                    #checks if the username needs to be changed
                                    if current_username != new_username:
                                        conn = sqlite3.connect("information.db")
                                        cur = conn.cursor()
                                        cur.execute("UPDATE users SET username=? WHERE username=?", (new_username, current_username))
                                        conn.commit()
                                        conn.close()
                                        messagebox.showinfo(title = "Success", message = "Username has been changed successfully")
                                    #an error message will pop up if any of the requirements are not satisfied
                                    else:
                                        messagebox.showerror(title="Error", message="New username must not be identical to current username")
                                        self.new_username_entry.delete(0,END)
                                        self.confirm_new_username_entry.delete(0,END)
                                else:
                                    messagebox.showerror(title = "Error", message = "Current password entered is incorrect")
                                    self.new_username_entry.delete(0,END)
                                    self.confirm_new_username_entry.delete(0,END)
                            else:
                                messagebox.showerror(title = "Error", message = "New username must be at least 5 characters long")
                                self.new_username_entry.delete(0,END)
                                self.confirm_new_username_entry.delete(0,END)
                        else:
                            messagebox.showerror(title = "Error", message = "New username is too long")
                            self.new_username_entry.delete(0,END)
                            self.confirm_new_username_entry.delete(0,END)
                    else:
                        messagebox.showerror(title = "Error", message = "User not found")
                        self.new_username_entry.delete(0,END)
                        self.confirm_new_username_entry.delete(0,END)
                else:
                    messagebox.showerror(title= "Error",message = "New username must be identical to confirm new password")
                    self.new_username_entry.delete(0,END)
                    self.confirm_new_username_entry.delete(0,END)
            else:
                messagebox.showerror(title= "Error",message = "None of the entry boxes should be empty")
                self.new_username_entry.delete(0,END)
                self.confirm_new_username_entry.delete(0,END)
        else:
            messagebox.showerror(title = "Error",message="Database does not exist")
            self.new_username_entry.delete(0,END)
            self.confirm_new_username_entry.delete(0,END)

    #method to go back to login page
    def go_back(self):
        call(["python","FitPro.py"])
        self.close_everything()

    #method to delete every widget before closing window
    def close_everything(self):
        children = self.winfo_children()
        for widget in children:
            widget.destroy()
        self.destroy()

#run window
if __name__ == "__main__":
    app = window()
    app.mainloop()

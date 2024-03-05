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
        self.geometry("800x410")
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
        self.change_password_button = Button(self, "Change password", self.change_password_get_info,x=200,y=350)
        self.change_username_button = Button(self, "Change username", self.change_username_get_info,x=560,y=350)
        self.change_password_label = Label(self,"Change password", self.title_font, x=170,y=90)
        self.change_username_label = Label(self,"Change username", self.title_font,x=550,y=90)
        self.current_username_value_label1 = Label(self,"Current username", self.header_font,x=30,y=150)
        self.current_password_value_label1 = Label(self,"Current password", self.header_font,x=30,y=200)
        self.current_username_value_label2 = Label(self,"Current username", self.header_font,x=390,y=150)
        self.current_password_value_label2 = Label(self,"Current password", self.header_font,x=390,y=200)
        self.new_password_value_label = Label(self,"New password", self.header_font,x=30,y=250)
        self.new_username_value_label = Label(self,"New username", self.header_font,x=390,y=250)
        self.confirm_new_password_value_label = Label(self,"Confirm new\npassword", self.header_font,x=40,y=290)
        self.confirm_new_username_value_label = Label(self,"Confirm new\nusername", self.header_font,x=400,y=290)
        self.current_username_value_entry1 = Entry(self, "", self.current_username1,x=200,y=150)
        self.current_password_value_entry1 = Entry(self, "*", self.current_password1,x=200,y=200)
        self.current_username_value_entry2 = Entry(self, "", self.current_username2,x=560,y=150)
        self.current_password_value_entry2 = Entry(self, "*", self.current_password2,x=560,y=200)
        self.new_password_value_entry = Entry(self, "*", self.new_password,x=200,y=250)
        self.new_username_value_entry = Entry(self, "", self.new_username,x=560,y=250)
        self.confirm_new_password_value_entry = Entry(self, "*", self.confirm_new_password,x=200,y=300)
        self.confirm_new_username_value_entry = Entry(self, "", self.confirm_new_username,x=560,y=300)

    def change_password_get_info(self):
        self.current_username_value = self.current_username1.get()
        self.current_password_value = self.current_password1.get()
        self.new_password_value = self.new_password.get()
        self.confirm_new_password_value = self.confirm_new_password.get()
        #get length of new password
        self.new_password_value_length = len(self.new_password_value)
        self.current_username_value = self.current_username_value.lower()
        #call next method
        self.check_lengths_change_password()

    def check_lengths_change_password(self):
        #checks if any entries are empty or not
        if self.current_username_value and self.current_password_value and self.new_password_value and self.confirm_new_password_value != "":
            #checks length of new password
            if self.new_password_value_length < 15:
                if self.new_password_value_length >= 5:
                    self.check_identical_change_password()
                #an error message will pop up if any of the requirements are not satisfied
                else:
                    messagebox.showerror(title = "Error", message = "New password must be at least 5 characters long")
                    self.new_password_value_entry.delete(0,END)
                    self.confirm_new_password_value_entry.delete(0,END)
            else:
                messagebox.showerror(title = "Error", message = "New password is too long")
                self.new_password_value_entry.delete(0,END)
                self.confirm_new_password_value_entry.delete(0,END)
        else:
            messagebox.showerror(title= "Error",message = "None of the entry boxes should be empty")
            self.new_password_value_entry.delete(0,END)
            self.confirm_new_password_value_entry.delete(0,END)

    def check_identical_change_password(self):
        #checks if current password matches confirm new password
        if self.new_password_value == self.confirm_new_password_value:
            self.special_and_capital_change_password()
        #an error message will pop up if any of the requirements are not satisfied
        else:
            messagebox.showerror(title= "Error",message = "New password must be identical to confirm new password")
            self.new_password_value_entry.delete(0,END)
            self.confirm_new_password_value_entry.delete(0,END)

    def special_and_capital_change_password(self):
        #check if there is at least one capital letter and special character in new password, 
        #the "\" allows the character after it to be accepted as a character
        if (re.search(r'[\\!@#$%()?^&*()_\-+={}[\]|\/:;"\'<>,.]', self.new_password_value)):
            if (re.search(r'[A-Z]', self.new_password_value)):
                self.check_details_match_change_password()
            #an error message will pop up if any of the requirements are not satisfied
            else:
                messagebox.showerror(title="Error", message="Password must contain at least one capital letter")
                self.new_password_value_entry.delete(0,END)
                self.confirm_new_password_value_entry.delete(0,END)  
        else:
            messagebox.showerror(title="Error", message="Password must contain at least one special character")
            self.new_password_value_entry.delete(0,END)
            self.confirm_new_password_value_entry.delete(0,END)  
    
    def check_details_match_change_password(self):
        conn = sqlite3.connect("information.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?",(self.current_username_value,))
        user = cur.fetchone()
        conn.close()
        #checks if account with entered username exists
        if user is not None:
            correct_password = user[2]
            #hash current password and new password entries so that current password can be compared to the hashed password in the database,
            #and so the new password can be added into the database as a hashed string, for security
            h = hashlib.sha256()
            h.update(self.current_password_value.encode("utf-8"))
            hashed_current_password = h.hexdigest()
            h = hashlib.sha256()
            h.update(self.new_password_value.encode("utf-8"))
            self.hashed_new_password = h.hexdigest()
            #checks if current password matches with password in database
            if correct_password == hashed_current_password:
                self.change_password()
            #an error message will pop up if any of the requirements are not satisfied
            else:
                messagebox.showerror(title = "Error", message = "Current password entered is incorrect")
                self.new_password_value_entry.delete(0,END)
                self.confirm_new_password_value_entry.delete(0,END)
        else:
            messagebox.showerror(title = "Error", message = "User not found")
            self.new_password_value_entry.delete(0,END)
            self.confirm_new_password_value_entry.delete(0,END)

    def change_password(self):
        #check if new password is the same as the current password
        if self.current_password_value != self.new_password_value:
            conn = sqlite3.connect("information.db")
            cur = conn.cursor()
            cur.execute("UPDATE users SET password=? WHERE username=?", (self.hashed_new_password, self.current_username_value))
            conn.commit()
            conn.close()
            messagebox.showinfo(title = "Success", message = "Password has been changed successfully")
            self.current_username_value_entry2.delete(0,END)
            self.current_password_value_entry2.delete(0,END)
            self.new_password_value_entry.delete(0,END)
            self.confirm_new_password_value_entry.delete(0,END)
        #an error message will pop up if the requirements are not satisfied 
        else:
            messagebox.showerror(title="Error", message="New password must not be identical to current password")
            self.new_password_value_entry.delete(0,END)
            self.confirm_new_password_value_entry.delete(0,END)

    def change_username_get_info(self):
        #get inputs
        self.current_username_value1 = self.current_username2.get()
        self.current_password_value1 = self.current_password2.get()
        self.new_username_value = self.new_username.get()
        self.confirm_new_username_value = self.confirm_new_username.get()
        #get length of new username
        self.new_username_value_length = len(self.new_username_value)
        self.current_username_value1 = self.current_username_value1.lower()
        self.new_username_value = self.new_username_value.lower()
        self.confirm_new_username_value = self.confirm_new_username_value.lower()
        #call next method
        self.check_identical_change_username()

    def check_identical_change_username(self):
        #checks if any entries are empty or not
        if self.current_username_value1 and self.current_password_value1 and self.new_username_value and self.confirm_new_username_value != "":
            #checks if current username matches confirm new username
            if self.new_username_value == self.confirm_new_username_value:
                self.change_username()
            #an error message will pop up if any of the requirements are not satisfied
            else:
                messagebox.showerror(title= "Error",message = "New username must be identical to confirm new username")
                self.new_username_value_entry.delete(0,END)
                self.confirm_new_username_value_entry.delete(0,END)
        else:
            messagebox.showerror(title= "Error",message = "None of the entry boxes should be empty")
            self.new_username_value_entry.delete(0,END)
            self.confirm_new_username_value_entry.delete(0,END)

    def change_username(self):
        conn = sqlite3.connect("information.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?",(self.current_username_value1,))
        user = cur.fetchone()
        conn.close()
        #checks if account with entered username exists
        if user is not None:
            #checks length of new username
            if self.new_username_value_length < 15:
                if self.new_username_value_length >= 5:
                    correct_password = user[2]
                    #hash current password entry so that it can be compared to the hashed password in the database
                    h = hashlib.sha256()
                    h.update(self.current_password_value1.encode("utf-8"))
                    hashed_current_password = h.hexdigest()
                    #checks if current password matches with password in database
                    if hashed_current_password == correct_password:
                        #checks if the username needs to be changed
                        if self.current_username_value1 != self.new_username_value:
                            conn = sqlite3.connect("information.db")
                            cur = conn.cursor()
                            cur.execute("UPDATE users SET username=? WHERE username=?", (self.new_username_value, self.current_username_value1))
                            conn.commit()
                            conn.close()
                            messagebox.showinfo(title = "Success", message = "Username has been changed successfully")
                            self.current_username_value_entry2.delete(0,END)
                            self.current_password_value_entry2.delete(0,END)
                            self.new_username_value_entry.delete(0,END)
                            self.confirm_new_username_value_entry.delete(0,END) 
                        #an error message will pop up if any of the requirements are not satisfied
                        else:
                            messagebox.showerror(title="Error", message="New username must not be identical to current username")
                            self.new_username_value_entry.delete(0,END)
                            self.confirm_new_username_value_entry.delete(0,END)
                    else:
                        messagebox.showerror(title="Error", message="Current password entered is incorrect")
                        self.new_username_value_entry.delete(0,END)
                        self.confirm_new_username_value_entry.delete(0,END)
                else:
                    messagebox.showerror(title = "Error", message = "New username must be at least 5 characters long")
                    self.new_username_value_entry.delete(0,END)
                    self.confirm_new_username_value_entry.delete(0,END)
            else:
                messagebox.showerror(title = "Error", message = "New username is too long")
                self.new_username_value_entry.delete(0,END)
                self.confirm_new_username_value_entry.delete(0,END)
        else:
            messagebox.showerror(title = "Error", message = "User not found")
            self.new_username_value_entry.delete(0,END)
            self.confirm_new_username_value_entry.delete(0,END)
            
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

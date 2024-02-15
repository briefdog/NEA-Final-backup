#import libraries
import customtkinter as ctk
import sqlite3
from subprocess import call
from tkinter import messagebox
from tkinter import *
import hashlib
import os

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
        self.geometry("350x300")
        #prevent user from resizing window
        self.resizable(False, False)

        #use entries as variables
        self.deleteaccount_username = StringVar()
        self.deleteaccount_password = StringVar()

        #create font
        self.title_font = Font("Helvetica", 20, "bold")
        self.header_font = Font("Helvetica", 18, "bold" )
        self.intructions_font = Font("Helvetica", 12,"bold" )

        #method called when user wants to close the window
        self.protocol("WM_DELETE_WINDOW", self.close_everything)

        #create and place widgets
        self.delete_button = Button(self, "Delete", self.delete_account, x=140, y=200)
        self.username_entry = Entry(self, "", self.deleteaccount_username, x=140, y=120)
        self.password_entry = Entry(self, "*", self.deleteaccount_password, x=140, y=160)
        self.deleteaccount_label = Label(self, "Delete Account", x=130, y=80, font=self.title_font)
        self.username_label = Label(self, "Username", x=30, y=120, font=self.header_font)
        self.password_label = Label(self, "Password", x=30, y=160, font=self.header_font)
        self.return_button = Button(self, "Return to login page", self.back, x=130, y=20)
        self.instructions_label = Label(self, "Enter username and password of\n the account that you wish to delete", x=70, y=250, font=self.intructions_font)

    #method to go to login page
    def back(self):
        call(["python","FitPro.py"])
        self.close_everything()

    #delete account if username and password matches
    def delete_account(self):
        #get all values from entry boxes
        delete_username = self.deleteaccount_username.get()
        delete_username = delete_username.lower()
        delete_password = self.deleteaccount_password.get()
        if os.path.isfile("information.db"):
            #connect to database
            conn = sqlite3.connect("information.db")
            #I encountered an error where the foreign key constraint was not working, but this helped: https://stackoverflow.com/questions/13641250/sqlite-delete-cascade-not-working
            conn.execute("PRAGMA foreign_keys = ON")
            cur = conn.cursor()
            #if the username matches with a username in the database, it will continue
            cur.execute("SELECT * FROM users WHERE username = ?",(delete_username,))
            password_hash = cur.fetchone()
            if password_hash is not None:
                #hash password entered by user so it can be compared with hashed password in database
                h = hashlib.sha256()
                h.update(delete_password.encode("utf-8"))
                delete_password = h.hexdigest()
                #compare the password entered by user (now hashed) with the hashed password in database
                if delete_password == password_hash[2]:
                    #if the passwords match, the user will be asked if they really want to delete their account, and if user chooses "yes", account will be deleted, if the user chooses "no", account will not be deleted
                    msg_box = messagebox.askquestion(title="Alert!",message = "Are you sure you want to delete the account?")
                    if msg_box == "yes":
                        cur.execute("DELETE FROM users WHERE username = ?",(delete_username,))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo(title = "Success", message = "Account has been deleted")
                #if passwords do not match, an error message will pop up
                else:
                    messagebox.showerror(title= "Error", message = "Invalid password")
            #if usernames do not match, an error message will pop up
            else:
                messagebox.showerror(title="Error", message="No account has been found")
        else:
            messagebox.showerror(title = "Error",message="Database does not exist")

        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)

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

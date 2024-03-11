#I used this video to learn how to use API's with python, requests and json: https://www.youtube.com/watch?v=bKCORrHbutQ&t=14s
#I found this website online to fetch food information from: https://world.openfoodfacts.org/
#I used these for documentation: https://openfoodfacts.github.io/openfoodfacts-server/api/ref-v2/ , https://openfoodfacts.github.io/openfoodfacts-server/api/tutorial-off-api/
#API says that one barcode scan equals one API call
#100 calls a minute
#This API has access to 3,063,704 products from the world (numbers may change), as of right now, meaning products are limited
#I tested the API by taking barcodes from https://world.openfoodfacts.org/

#import requests for HTTP requests
import requests

#import GUI needed
import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
from tkinter import font
import customtkinter as ctk
#import libraries to access images from API
from PIL import Image, ImageTk
from io import BytesIO

import os

#the image is displayed bigger when it is converted into tkinter format than in customtkinter,
#so warning messages may come up in the terminal as I am using the tkinter format in customtkinter, even though it works

#import subprocess for switching between python scripts
import subprocess
from subprocess import call

#class for changing font of labels
class Font(ctk.CTkFont):
    def __init__(self, family, size, weight):
        super().__init__(family=family, size=size, weight=weight)
        
#classes for creating different widgets that will be used
class Entry(ctk.CTkEntry):
    def __init__(self, master, show, textvariable, **kwargs):             
        super().__init__(master, show=show , textvariable=textvariable)
        self.place(**kwargs)

class Label(ctk.CTkLabel):
    def __init__(self, master, text,font, **kwargs):
        super().__init__(master, text=text, font=font)
        self.place(**kwargs)

class Button(ctk.CTkButton):
    def __init__(self, master, text, command, **kwargs):
        super().__init__(master, text=text, command=command)
        self.place(**kwargs)

#class to create image label
class ImageLabel(ctk.CTkLabel):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text)
        self.place(**kwargs)

#class for window to run
class window(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FitPro")
        self.geometry("820x600")
        self.resizable(False, False)
        #makes font "bold"
        self.title_font = Font("Helvetica", 20, "bold")

        # Create and add widgets with custom placement
        self.title_label = Label(self, "Enter product code here:", x=100, y=50, font=self.title_font)
        self.button = Button(self, "Find information", self.getfoodinfo, x=100, y=150)
        self.button = Button(self, "Go back to homepage", self.goback, x=10,y=10)
        #image label created so it can be configured in the fetch_and_display_image label method to display an image
        self.image_label = ImageLabel(master=self, text="", x=500, y=200)

        # text variable
        self.productcode = StringVar()
        self.entry = Entry(self, "", self.productcode, x=100, y=100)

    #method will fetch data from API
    def getfoodinfo(self):
        product_input = self.productcode.get()
        url = f"https://world.openfoodfacts.org/api/v0/product/{product_input}.json"    
        try:
            response = requests.get(url)
        #if there is no internet connection, error box will appear
        except:
            messagebox.showerror(title = "Error", message = "Network error\nMake sure to check your internet connection")
            return
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('status', '') == 1:
                    #get dictionaries
                    product_info = data.get('product', {})
                    nutrition_info = product_info.get('nutriments', {})
                    nutrition_score = product_info.get('nutriscore_data', {})
                    #get image url from API
                    self.image_url = product_info.get('image_url', 'N/A')
                    
                    #learned winfo_children() from https://www.youtube.com/watch?v=A6m7TmjuNzw
                    #previous labels get deleted and new labels get added dynamically
                    for widget in self.winfo_children():
                        if isinstance(widget, Label) and widget != self.title_label:
                            widget.destroy()

                    #Get data from dictionaries and then display the data as labels, 
                    #I used json data dump in another file, and documentation to help find the dictionaries with data
                    product_name_label = Label(self, f"Product name: {product_info.get('product_name', 'N/A')}",font=("Helvetica", 16),x=100,y=200)

                    brand_label = Label(self, f"Brand: {product_info.get('brands', 'N/A')}", font=("Helvetica", 16),x=100,y=230)

                    categories_label = Label(self, f"Categories: {', '.join(product_info.get('categories_tags', ['N/A'])[:2])}", font=("Helvetica", 16), x=100, y=260)

                    allergens_label = Label(self, f"Allergens: {', '.join(product_info.get('allergens_tags', 'N/A'))}",font=("Helvetica", 16),x=100,y=290)

                    nutrition_info_label = Label(self, "Nutrition Information:", font=("Helvetica", 16),x=100,y=320)

                    energy_label = Label(self, f"Energy: {nutrition_info.get('energy-kcal_100g', 'N/A')} kcal/100g",font=("Helvetica", 16),x=100,y=350)

                    fat_label = Label(self, f"Fat: {nutrition_info.get('fat_100g', 'N/A')} g/100g", font=("Helvetica", 16),x=100,y=380)

                    carbohydrates_label = Label(self,f"Carbohydrates: {nutrition_info.get('carbohydrates_100g', 'N/A')} g/100g",font=("Helvetica", 16),x=100,y=410)

                    proteins_label = Label(self, f"Proteins: {nutrition_info.get('proteins_100g', 'N/A')} g/100g",font=("Helvetica", 16),x=100,y=440)
                
                    nutri_score = Label(self, f"Nutrition Score: {nutrition_score.get('grade', 'N/A')}",font=("Helvetica", 16),x=100,y=470)
                    #go to display image method
                    self.fetch_and_display_image()
                #show error messages if there are any problems connecting to the api or retrieving the information
                else:
                    messagebox.showerror(title = "error", message = "Product not found")
            except requests.exceptions.JSONDecodeError as e:
                messagebox.showerror(title = "Error", message = f"Error decoding JSON: {e}\n{response.content}")
        else:
            messagebox.showerror(title = "Error", message = f"Error: {response.status_code}\n{response.content}")
        self.entry.delete(0, END)

    def fetch_and_display_image(self):
        try:
            response = requests.get(self.image_url)
            if response.status_code == 200:
                #take response as binary
                image_data = response.content
                #create PIL image from binary data
                img = Image.open(BytesIO(image_data))
                #convert the PIL image to tkinter format
                #This video was used to help with pillow and ImageTk https://www.youtube.com/watch?v=kjc53i4xUmw
                photo = ImageTk.PhotoImage(img)
                #change label so it displays image
                self.image_label.configure(image=photo)
                self.image_label.image = photo
            
            else:
                messagebox.showerror(title = "Error",message="Failed to fetch image")
        except: 
            #if image url for any reason is invalid, the user will not see an error
            pass

    #go back to homepage
    def goback(self):
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





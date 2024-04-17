# src/registration_page.py
from tkinter import ttk, StringVar, Label, Entry, Button, messagebox
from base_window import BaseWindow
from database_handler import DatabaseHandler
from PIL import Image, ImageTk
from tkinter import ttk, Tk
import tkinter as tk
import os
# import tkinter.messagebox as messagebox


class RegistrationPage(BaseWindow):
    def __init__(self, root, database_handler, on_registration_success, on_login_success):
        super().__init__(root, "Phishing Detection Registration Page")
        self.database_handler = database_handler
        self.on_registration_success = on_registration_success
        self.on_login_success = on_login_success
        self.message_var = StringVar()
        
        icon_path = os.path.abspath("twitter_logo.png")  # Replace with the path to your icon file in .ico format
        self.root.iconbitmap(icon_path)
        self.icon_register = ImageTk.PhotoImage(file=icon_path)
        self.root.iconphoto(True, self.icon_register)
        self.root.geometry('800x600')

        

        self.create_widgets()
        
      
    def create_widgets(self):
        

        # Increase the font size
        title_font = ('Helvetica', 22)

        ttk.Label(self.root, text="Register New User", font=title_font).grid(row=0, column=0, columnspan=2, pady=40)

        ttk.Label(self.root, text="Username:", font=('Helvetica', 12)).grid(row=1, column=0, padx=10, pady=15, sticky='e')
        self.username_entry = ttk.Entry(self.root, width=40, font=('Helvetica', 12))
        self.username_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(self.root, text="Password:", font=('Helvetica', 12)).grid(row=2, column=0, padx=10, pady=15, sticky='e')
        self.password_entry = ttk.Entry(self.root, width=40, show='*', font=('Helvetica', 12))
        self.password_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(self.root, text="Name:", font=('Helvetica', 12)).grid(row=3, column=0, padx=10, pady=15, sticky='e')
        self.name_entry = ttk.Entry(self.root, width=40, font=('Helvetica', 12))
        self.name_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')
         
        ttk.Label(self.root, text="Email:", font=('Helvetica', 12)).grid(row=4, column=0, padx=10, pady=15, sticky='e')
        self.email_entry = ttk.Entry(self.root, width=40, font=('Helvetica', 12))
        self.email_entry.grid(row=4, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(self.root, text="Phone:", font=('Helvetica', 12)).grid(row=5, column=0, padx=10, pady=15, sticky='e')
        self.phone_entry = ttk.Entry(self.root, width=40, font=('Helvetica', 12))
        self.phone_entry.grid(row=5, column=1, padx=10, pady=5, sticky='w')


        ttk.Label(self.root, text="Model Path:", font=('Helvetica', 12)).grid(row=6, column=0, padx=10, pady=15, sticky='e')
        self.model_path_entry = ttk.Entry(self.root, width=40, font=('Helvetica', 12))
        self.model_path_entry.grid(row=6, column=1, padx=10, pady=5, sticky='w')
        
        register_button = ttk.Button(self.root, text="Submit", command=self.register, width=20)
        register_button.grid(row=7, column=0, columnspan=6, pady=(20, 5), padx=10, sticky='n')  # Adjusted to use grid

        # Reset button to clear input box contents
        reset_button = ttk.Button(self.root, text="Reset", command=self.reset, width=20)
        reset_button.grid(row=7, column=1, columnspan=5, pady=(20, 5), padx=10, sticky='n')  # Adjusted to use grid

        
        
        # Message label to display registration status
        self.message_label = ttk.Label(self.root, textvariable=self.message_var, font=('Helvetica', 12), foreground='red')
        self.message_label.grid(row=8, column=0, columnspan=2, pady=10)
        # Center the content horizontally
        for i in range(2):
            self.root.grid_columnconfigure(i, weight=1)

        # Set weight to center columns for horizontal centering
        self.root.grid_columnconfigure(1, weight=1)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        model_path = self.model_path_entry.get()

        if username and password and name and email and phone and model_path:
            if not self.database_handler.check_user_exists(username, email, phone):
                self.database_handler.insert_user(username, password, name, email, phone, model_path)
                # Update the model path in the database
                # self.database_handler.update_model_path(username, model_path)
                if callable(self.on_registration_success):
                    self.on_registration_success()
                messagebox.showinfo("Registration Successful", "You have successfully registered!")
                self.root.destroy()  # Close the registration window
            
                 # Create a new Tk instance for LoginPage
                # from login_page import LoginPage   
                #  # Open the login window

                 
                # login_window = tk.Toplevel(self.root)
                # self.login_page = LoginPage(login_window, self.database_handler, self.on_login_success, self.on_registration_success)
                # self.login_page.create_widgets()
            else:
                  messagebox.showerror("Registration Failed", "User already exists. Please choose a different username, email, or phone.")
        else:
              messagebox.showerror("Registration Failed", "Please fill in all fields.")

    def reset(self):
        # Clear input box contents
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.model_path_entry.delete(0, tk.END)
        # login_page_instance = LoginPage(self.root, self.database_handler, self.on_login_success, self.on_registration_success)
        
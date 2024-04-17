# src/login_page.py
from tkinter import ttk, messagebox, CENTER
from PIL import Image, ImageTk
from base_window import BaseWindow
from database_handler import DatabaseHandler
import phishing_detector_app
from registration_page import RegistrationPage  # Make sure to import RegistrationPage
import tkinter as tk
from phishing_detector_app import PhishingDetectorApp
import os
# ...

class LoginPage(BaseWindow):
    def __init__(self, root, database_handler, on_login_success, on_registration_success):
        super().__init__(root, "Phishing Detection Login Page")  # Set the title
        self.database_handler = database_handler
        self.on_login_success = on_login_success
        self.on_registration_success = on_registration_success
        # self.root.attributes('-fullscreen', True)
 
        icon_path = "twitter_logo.png"
        icon = Image.open(icon_path)
        icon = icon.resize((200, 150), resample=Image.LANCZOS)  # Adjust the size as needed

        self.icon_login = ImageTk.PhotoImage(icon)
        self.root.iconphoto(True, self.icon_login)
           
        # Twitter logo and heading
        
        
       
        
        self.logo_label = ttk.Label(root, image=self.icon_login)
        self.logo_label.grid(row=0, column=0, columnspan=6, pady=(40, 5), sticky='n')  # Centered at the top

        heading_label = ttk.Label(root, text="Phishing Detection for Twitter", font=('Helvetica', 18))
        heading_label.grid(row=1, column=0, columnspan=6, pady=20, sticky='n')  # Centered

        # Username and password entry
        ttk.Label(root, text="Username:").grid(row=2, column=2, padx=5, pady=20, sticky='e')
        self.username_entry = ttk.Entry(root, width=35)
        self.username_entry.grid(row=2, column=3, padx=5, pady=2, sticky='w', columnspan=5)  # Spanning 5 columns

        ttk.Label(root, text="Password:").grid(row=3, column=2, padx=5, pady=20, sticky='e')
        self.password_entry = ttk.Entry(root, width=35, show='*')
        self.password_entry.grid(row=3, column=3, padx=5, pady=2, sticky='w', columnspan=5)  # Spanning 5 columns

        
         # ... (unchanged code)

        # Login button with increased size and margin
        login_button = ttk.Button(root, text="Login", command=self.login, width=20)
        login_button.grid(row=4, column=0, columnspan=5, pady=(10, 5), sticky='n')  # Centered with more padding

        # Register button with increased size and space
        register_button = ttk.Button(root, text="Register", command=self.open_registration, width=20)
        register_button.grid(row=4, column=2, columnspan=6, pady=(10, 5), sticky='n')  # Centered with more padding and space

       
        # ... (unchanged code)
        # Error message label
        self.error_label = ttk.Label(root, text="", foreground="red")
        self.error_label.grid(row=6, column=0, columnspan=6, pady=2, sticky='n')  # Centered
        
        # Center the content vertically
        for i in range(7):
            root.grid_rowconfigure(i, weight=0)

        # Set weight to center rows for vertical centering
        root.grid_rowconfigure(3, weight=0)
        root.grid_rowconfigure(4, weight=0)
        root.grid_rowconfigure(5, weight=0)
        root.grid_rowconfigure(6, weight=0)

        # Center the content horizontally
        for i in range(6):
            root.grid_columnconfigure(i, weight=1)

    def login(self):
        # Add your authentication logic here
        # For simplicity, let's assume any non-empty username and password is considered successful
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Check the username and password against the database
        if username and password:
            if self.database_handler.check_credentials(username, password):
                model_path = self.database_handler.get_model_path(username)
                
                if model_path:
                    first_model_path = model_path[0] 
                    print("Model Path:", model_path)
                     # Display a success message
                    messagebox.showinfo("Login Successful", "You have successfully logged in!")
                    self.root.destroy()
                    phishing_app_window = tk.Tk()
                    phishing_app = PhishingDetectorApp(phishing_app_window, model_path=model_path)
                    # phishing_app = PhishingDetectorApp(phishing_app_window,  self.database_handler,  self.on_login_success)
                    phishing_app.create_widgets()
               
                else:
                    # print("Model path not Provided.")
                    self.error_label.config(text="Model path not Provided.")
            
            else:
                # print("Invalid crendentials.")
                self.error_label.config(text="Invalid crendentials.")
        else:
            # Display an error message
            self.error_label.config(text="Please enter both username and password")


        
    def open_registration(self):
        registration_window = tk.Toplevel(self.root)
        self.registration_page = RegistrationPage(registration_window, self.database_handler, self.on_registration_success, self.on_login_success)
        self.registration_page.create_widgets()
        
    def show(self):
        super().show()

    def hide(self):
        super().hide()

    def destroy(self):
        super().destroy()
 

    

   
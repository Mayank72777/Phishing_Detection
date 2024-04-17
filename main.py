import tkinter as tk
import pandas as pd
from database_handler import DatabaseHandler
from login_page import LoginPage
from phishing_detector_app import PhishingDetectorApp
from registration_page import RegistrationPage
import mysql.connector as connector

class AppManager:
    def __init__(self, root, model_path=None):
        self.root = root
        self.root.geometry('800x600')

        self.database_handler = DatabaseHandler(
            host='localhost',
            port='3306',
            user='root',
            password='Priyam00',
            database='Phishing_Detection'
        )
        self.database_handler.connect()
        self.database_handler.create_user_table()

        self.login_page = LoginPage(root, self.database_handler, self.on_login_success, self.on_registration_success)
        # self.registration_page = RegistrationPage(self.root, self.database_handler, self.on_registration_success, self.on_login_success)
        self.registration_page = None
        self.phishing_detector_app = None

        self.show_login_page()

   

    def on_login_success(self):
        self.login_page.hide()
        self.show_phishing_detector_app()

    def on_registration_success(self):
        print("Registration Successful")
        if self.registration_page:
           self.registration_page.destroy()
        self.show_login_page()

    def show_login_page(self):
        self.login_page.show()
        if self.registration_page:
            self.registration_page.destroy()
        if self.phishing_detector_app:
            self.phishing_detector_app.destroy()

    
    def show_phishing_detector_app(self):
       if not self.phishing_detector_app and self.model_path:
            model_path = self.model_path[0]
            
            self.phishing_detector_app = PhishingDetectorApp(self.root, model_path=self.model_path)
            self.phishing_detector_app.create_widgets()
            # self.phishing_detector_app.show()
    
    
    def create_model_and_train(self, dataset_path):
        # Load and preprocess the dataset
        # Add your dataset loading and preprocessing logic here
        df = pd.read_csv(dataset_path)
        processed_df = self.preprocess_dataset(df, 'custom_dataset_type')

        # Train the model
        model = self.train_model(processed_df['text'], processed_df['label'])
        self.loaded_model = model  # Update the loaded model

        # Print dataset information
        print("Dataset Description:")
        print(processed_df.describe())

        # Print training results
        print("Training Results:")
        # Add your training result information here

if __name__ == "__main__":
    root = tk.Tk()
    model_path = ['Compromised_IOCs.csv','phishing_site_urls.csv', 'malicious_phish.csv']
    
    
    app_manager = AppManager(root, model_path=model_path)
    root.mainloop()
    # root.protocol("WM_DELETE_WINDOW", app_manager.database_handler.close_connection)  # Close the database connection when the window is closed
    # try:
    #     root.mainloop()
    # except Exception as e:
    #     print(f"An unexpected error occurred in the main loop: {e}")

    app_manager.database_handler.close_connection()

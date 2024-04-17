# src/database_handler.py
import tkinter.messagebox as messagebox
import mysql.connector 
from mysql.connector import Error
import os

class DatabaseHandler:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                port = self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to MySQL database")
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
             # Display an error message on the same window
            messagebox.showerror("Connection Error", "Error connecting to the database. Please check your connection.")

    def close_connection(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Connection closed")

    def create_user_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255),
                password VARCHAR(255),
                name VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(20),
                model_path VARCHAR(255)
            )
        ''')
        cursor.close()

    def insert_user(self, username, password, name, email, phone, model_path):
        try:
            # Check if the user already exists
            if self.check_user_exists(username, email, phone):
                return False  # User already exists, return False
            
            cursor = self.conn.cursor()
            query = "INSERT INTO users (username, password, name, email, phone, model_path) VALUES (%s, %s, %s, %s, %s,%s)"
            values = (username, password, name, email, phone, model_path)

            # Execute the query
            cursor.execute(query, values)
            self.conn.commit()
            cursor.close()
      
            return True  # Insertion successful
        except Error as e:
            print(f"Error: {e}")
            return False  # Return False in case of an error
        # finally:
        # Close the cursor and connection
            
            # self.connection.close()
        
    # In database_handler.py
    def check_user_exists(self, username, email, phone):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s OR email = %s OR phone = %s"
        values = (username, email, phone)
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()
        return result is not None


    def check_credentials(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def get_model_path(self, username):
        cursor = self.conn.cursor()
        cursor.execute('SELECT model_path FROM users WHERE username = %s', (username,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]  # Assuming the model_path is stored in the 'model_path' column
        else:
            return None  # Return None if no model path is found
        
def update_model_path(self, username, model_path):
        try:
            query = "UPDATE users SET model_path = %s WHERE username = %s"
            values = (model_path, username)
            self.conn.cursor().execute(query, values)
            self.connection.commit()
            print("Model path updated successfully.")
        except Exception as e:
            print(f"Error updating model path: {e}")

    # ... (existing code)
# **********************************************************************************************




   

# src/phishing_detector_app.py

import tkinter as tk
from tkinter import ttk, scrolledtext
import traceback 
from PIL import Image, ImageTk
from base_window import BaseWindow
import joblib
import tweepy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder





class PhishingDetectorApp(BaseWindow):
   
    def __init__(self, root, model_path=None, csv_paths=None):
        super().__init__(root, "Phishing Detector App")
        self.logo_label = None
        icon = Image.open("twitter_logo.png")
        icon = icon.resize((175, 125), resample=Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.BICUBIC)
        self.icon = ImageTk.PhotoImage(icon)
        self.root.iconphoto(True, self.icon)
        self.root.geometry('800x600')
        self.model_path = model_path
        self.processed_df = None
        self.label_encoder = LabelEncoder()  # Initialize label_encoder as an instance variable

        #Load model
        self.loaded_model = None
        if model_path:
            try:
                if isinstance(model_path, list) and len(model_path) > 0:
                    model_path = model_path[0]
                self.loaded_model = joblib.load(model_path)
                if self.loaded_model is None:
                    print(f"Error: loaded model is none")
                else:
                    print("Model loaded successfully.")
            except FileNotFoundError:
                print(f"Error: Model file not found at {model_path}.")
            except Exception as e:
                print(f"Error loading model : {e}")
                traceback.print_exc()
                return
        else:
             print("Warning: No model path provided.")

        # Load and train models on the specified CSV datasets
        self.loaded_models = []
        if csv_paths:
            for path, dataset_type in csv_paths:
                try:
                    # Load the dataset from CSV
                    df = pd.read_csv(path)
                    df.head()
                    # Preprocess the dataset
                    self.processed_df = self.preprocess_dataset(df, dataset_type)
                    if self.processed_df is not None:
                    # Train a model using the processed dataset
                        model = self.train_model(self.processed_df['text'], self.processed_df['label'])

                        self.loaded_models.append(model)
                except Exception as e:
                    print(f"Error loading/training model using data from {path}: {e}")

        self.result_message_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=4)
        self.create_widgets()

    def create_widgets(self):
        
        
        try:
            # If model_path is a list of paths, choose the first one
            if isinstance(self.model_path, list) and len(self.model_path) > 0:
                self.model_path = self.model_path[0]

            # Load the model using the corrected model_path
            if self.model_path:
                # self.model = joblib.load(self.model_path)
                print("Model loaded successfully")
            
            else:
                print("Warning: No model path provided.")
                
        except Exception as e:
            print(f"Error loading model: {e}")
         
    # Logo label
        self.logo_label = ttk.Label(self.root, image=self.icon)
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=(50, 10))  # Center vertically
        

    # Text entry for user to input a tweet
        self.tweet_entry_label = ttk.Label(self.root, text="Enter Tweet\\URL")
        self.tweet_entry_label.grid(row=1, column=0, columnspan=2)

        self.tweet_entry = ttk.Entry(self.root, width=80)
        self.tweet_entry.grid(row=2, column=0, columnspan=2, pady=10)  # Center vertically

    # Button to predict phishing
        self.predict_button = ttk.Button(self.root, text="Predict", command=self.predict_phishing)
        self.predict_button.grid(row=3, column=0, columnspan=2, pady=20)  # Center vertically

    # Button to fetch tweets
        self.fetch_tweets_button = ttk.Button(self.root, text="Fetch Tweets", command=self.fetch_tweets)
        self.fetch_tweets_button.grid(row=4, column=0, columnspan=2, pady=10)  # Center vertically

    # Button to search tweets or URLs
        self.search_tweet_button = ttk.Button(self.root, text="Search Tweet", command=self.search_tweet)
        self.search_tweet_button.grid(row=5, column=0, columnspan=2, pady=10)  # Center vertically
    
     # Result label
        self.result_label = ttk.Label(self.root, text="")
        self.result_label.grid(row=6, column=0, columnspan=2, pady=10)  # Center vertically

        # self.output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=10)
        # self.output_text.grid(row=6 , column=0, columnspan=2, pady=10)  # Center vertically
        
        self.result_message_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=8)
        self.result_message_box.grid(row=6, column=0, columnspan=2, pady=10)  
        
        # Center vertically
        # Center the content horizontally
        for i in range(2):
         self.root.grid_columnconfigure(i, weight=1)

     # Set weight to center columns for horizontal centering
        self.root.grid_columnconfigure(1, weight=1)

        # Center horizontally
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))


    def preprocess_dataset(self, df, dataset_type):
        # Use the appropriate preprocessing function based on dataset_type
        
        # if dataset_type == 'twitter':
        #     return self.preprocess_twitter_dataset(df)
        if dataset_type == 'url':
            return self.preprocess_url_dataset(df)
        else:
            print(f"Unsupported dataset type: {dataset_type}")
            return None

    def preprocess_twitter_dataset(self, df):
        try:
            # Assuming each dataset has a column 'content' instead of 'text'
            if 'tweet' in df.columns:
                df['text'] = df['tweet']

            # Assuming each dataset has a column 'phishing_label' instead of 'label'
            if 'tags' in df.columns:
                df['label'] = df['tags']

            # Other preprocessing steps...

            # Keep only 'text' and 'label' columns
            processed_df = df[['text', 'label']]

            return processed_df
        except Exception as e:
            print(f"Error preprocessing Twitter dataset: {e}")
            return None

    def preprocess_url_dataset(self, df):
        try:

            # Assuming each dataset has a column 'content' instead of 'text'
            if 'url' in df.columns:
                df['text'] = df['url']

            # Assuming each dataset has a column 'phishing_label' instead of 'label'
            if 'type' in df.columns:
                df['label'] = df['type']

            # Other preprocessing steps...

            # Keep only 'text' and 'label' columns
            processed_df = df[['text', 'label']]

            return processed_df
        except Exception as e: 
            print(f"Error preprocessing URL dataset: {e}")
            return None
    


    def train_model(self, texts, labels):
            # Apply label encoding
        self.label_encoder.fit(labels)
        labels_encoded = self.label_encoder.transform(labels)
        
        print("Unique classes after fitting LabelEncoder:", self.label_encoder.classes_)

        # Create a pipeline with TF-IDF vectorizer and Naive Bayes classifier
        model = make_pipeline(TfidfVectorizer(), MultinomialNB())

        # Train the model on the provided texts and labels
        model.fit(texts, labels_encoded)

        return model

    def predict_phishing(self):
        # Get the tweet from the entry
        tweet = self.tweet_entry.get()
        
        
        
        # Check if the model is loaded successfully
        if self.loaded_model is None:
            print("Error: Model not loaded successfully.")
            return
        
        # Check if processed_df is None
        # if self.processed_df is None:
        #     print("Error: processed_df is None.")
        #     return
        if self.processed_df is None:
            self.result_message_box.delete(1.0, tk.END)
            self.result_message_box.insert(tk.END, "Safe to use")
        return
        
    # Fit the LabelEncoder
        if not hasattr(self.label_encoder, 'classes_'):
            self.label_encoder.fit(self.processed_df['label'])


        # Make prediction
        try:
            #  # Ensure that the LabelEncoder is fitted
            # if not hasattr(self.label_encoder, 'classes_'):
            #     raise ValueError("LabelEncoder is not fitted. Call 'fit' with appropriate arguments before using this estimator.")
            prediction_encoded= self.loaded_model.predict([tweet])
            print(f"Prediction array: {prediction_encoded}")
            
              # Inverse transform to get the original label
            predicted_labels = self.label_encoder.inverse_transform(prediction_encoded)
            print(f"Predicted labels: {predicted_labels}")
            
            
                    # Check if any of the specified labels are present in the prediction
            if any(label in predicted_labels for label in ['phishing', 'malware', 'defacement', 'scam']):
                result = "Not safe to use."
            else:
                result = "Safe to use."
            
        #     if "phishing" in prediction :
        #         result = "Phishing Detected! It is not safe to use."
        # # ...
        #     elif "malware" in prediction :
        #         result = "Malware Detected! It is not safe to use."
        # # ...
        #     elif "defacement" in prediction:
        #         result = "Defacement Detected! Unsafe activity detected."
            
        #     elif "scam" in prediction :
        #         result = "Scam Detected! It is not safe to use."
        # # ...
        #     else:
        #         result = "No phishing activity detected. It is safe to use."
        
   
        # ...
            # Display the result
                # self.result_label.config(text=result, foreground="red" if "Detected" in result else "green")
                # self.result_message_box.delete(1.0, tk.END)
                # self.result_message_box.insert(tk.END, result)
                
                        # Display the result
                self.result_message_box.delete(1.0, tk.END)
                self.result_message_box.insert(tk.END, result)
        
        except Exception as e:
            print(f"Error Predicting: {e}")


    def fetch_tweets(self):
        try:
        # Get the user's entered query
            query = self.tweet_entry.get()
        
            self.display_fetched_tweets(query)
        except Exception as e:
            print(f"An unexpected error occurred while fetching tweets: {e}")
        # Provide feedback to the user
     
    def search_tweet(self):
        dataset_path = "path_to_fetched_tweets_or_urls.csv"
        self.create_model_and_train(dataset_path)   
        
        
    def display_fetched_tweets(self, query):
        try:
        # # Twitter API credentials
            self.consumer_key = "bQbuQsZ20r17mRbf0JOTptJKx"
            self.consumer_secret = "i9DyZADZDnSLKBkXEu9BPK3dwvFSa0BnGRN19AJivSJwpsH9wC"
            self.access_token = "1731322316536315904-ZqH85mV0bfmQ4vKWmNpRpv2xSdz7DS"
            self.access_token_secret = "JLqb1mEcVUCttEhnIyFfdOkxQifTrklsnoXfJRjeJHx9L"

        # Authenticate with Twitter API
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            api = tweepy.API(auth)
            tweets = tweepy.Cursor(api.search, q=query, lang='en', tweet_mode='extended').items(5)
            # Display fetched tweets in the result label
            tweet_texts = [tweet.full_text for tweet in tweets]
             # Clear existing content of result_label
            self.result_message_box.delete(1.0, tk.END) 
            self.result_message_box.insert(tk.END, "\n".join(tweet_texts))# Clear existing content
            
    
        except tweepy.TweepError as e:
           print(f"TweepError: {e}")
    
        except Exception as e:
           print(f"An unexpected error occurred: {e}")
   



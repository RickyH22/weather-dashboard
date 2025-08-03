# app.py
"""Main application that uses the core modules"""

import os
from dotenv import load_dotenv
from tkinter import messagebox

from core.api import WeatherAPI
from core.storage import StorageManager
from core.processor import DataProcessor
from gui.main_window import MainWindow
from gui.app_controller import AppController

# Load environment variables
load_dotenv()
print("API key:", os.getenv("OPENWEATHERMAP_API_KEY"))

class WeatherApp:
    """Main application class"""
    
    def __init__(self):
        # Initialize core components
        try:
            self.api = WeatherAPI()
            self.storage = StorageManager("weather_history.json")
            self.processor = DataProcessor()
            
            # Initialize GUI controller
            self.controller = AppController(
                api=self.api,
                storage=self.storage,
                processor=self.processor
            )
            
        except Exception as e:
            messagebox.showerror("Initialization Error", str(e))
            raise
    
    def run(self):
        """Run the application"""
        self.controller.start()

if __name__ == "__main__":
    app = WeatherApp()
    app.run()

# In main_window.py

def __init__(self):
    # Your existing code...
    
    # Create tabs for each feature
    self.content_frame = ttk.Frame(self.notebook, padding="10")
    self.features_frame = ttk.Frame(self.notebook, padding="10")
    self.graphs_frame = ttk.Frame(self.notebook, padding="10")
    self.team_frame = ttk.Frame(self.notebook, padding="10")  # Replace settings_frame
    self.poetry_frame = ttk.Frame(self.notebook, padding="10")
    
    # Add the frames as tabs
    self.notebook.add(self.content_frame, text="Current Weather")
    self.notebook.add(self.features_frame, text="City Comparison")
    self.notebook.add(self.graphs_frame, text="Temperature Trends")
    self.notebook.add(self.team_frame, text="Our Team")  # Replace "Settings" with "Our Team"
    self.notebook.add(self.poetry_frame, text="Weather Poetry")
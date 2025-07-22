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
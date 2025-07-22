"""Controller that manages GUI components and event handlers"""

import re
import tkinter as tk
from tkinter import messagebox

from gui.main_window import MainWindow
from gui.components import SearchBar, WeatherDisplay
from features.city_comparison import CityComparison

class AppController:
    """Controls the GUI components and handles events"""
    
    def __init__(self, api, storage, processor):
        """Initialize with core components as dependencies"""
        self.api = api
        self.storage = storage
        self.processor = processor
        
        # Create main window
        self.window = MainWindow()
        
        # Set up GUI components
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Add search bar
        self.search_bar = SearchBar(self.window.header_frame, self.on_search)
        
        # Add weather display
        self.weather_display = WeatherDisplay(self.window.content_frame)
        
        # Add city comparison feature
        self.comparison = CityComparison(
            self.window.features_frame,  # You'll need to add this frame to your MainWindow
            self.api.fetch_weather,      # Pass the API fetch method
            self.processor.process_api_response  # Pass the processor method
        )
    
    def on_search(self, city):
        """Handle search event"""
        # Input validation
        if not city:
            messagebox.showinfo("Input Required", "Please enter a city name")
            return
        
        # Check for invalid characters
        if not re.match(r'^[A-Za-z\s\-,]+$', city):
            messagebox.showerror("Invalid Input", "City name should contain only letters, spaces, hyphens and commas")
            return
            
        # Normalize input (trim whitespace, capitalize)
        city = city.strip().title()
        
        try:
            print(f"Attempting to fetch weather for {city}...")
            weather_data = self.api.fetch_weather(city)
            print(f"API response received: {weather_data is not None}")
            
            if weather_data:
                # Process the data
                processed_data = self.processor.process_api_response(weather_data)
                
                # Update the display
                self.weather_display.update(processed_data)
                
                # Save to storage
                self.storage.save_weather(city, processed_data)
            else:
                messagebox.showerror("Error", f"Could not find weather data for '{city}'")
        except Exception as e:
            messagebox.showerror("Search Error", f"An error occurred: {str(e)}")
    
    def start(self):
        """Start the application window"""
        self.window.run()
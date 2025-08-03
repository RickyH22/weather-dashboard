"""Controller that manages GUI components and event handlers"""

import re
import tkinter as tk
from tkinter import messagebox

from gui.main_window import MainWindow
from gui.components import SearchBar, WeatherDisplay
from features.city_comparison import CityComparison
from features.temperature_graph import TemperatureGraph
from features.theme_switcher import ThemeSwitcher
from features.weather_poetry import WeatherPoetry
from features.team_feature import TeamFeature

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
        # Add search and theme switcher to header (always visible)
        self.search_bar = SearchBar(self.window.header_frame, self.on_search)
        self.theme_switcher = ThemeSwitcher(self.window.header_frame, self.window.root)
        
        # Add weather display to main content tab
        self.weather_display = WeatherDisplay(self.window.content_frame)
        
        # Add city comparison feature to its tab
        self.comparison = CityComparison(
            self.window.features_frame,
            self.api.fetch_weather,
            self.processor.process_api_response
        )
        
        # Add temperature graph feature (7-day forecast)
        self.temp_graph = TemperatureGraph(
            self.window.graphs_frame,
            self.api.fetch_forecast,  # This connects to your API forecast method
            None  # No storage needed for forecast data
        )
        
        # Add weather poetry feature
        self.weather_poetry = WeatherPoetry(
            self.window.poetry_frame,
            self.api.fetch_weather  # Use your existing fetch_weather method
        )
        
        # Add team feature
        self.team_feature = TeamFeature(self.window.team_frame)
        
        # Register for tab change events
        self.window.register_callback("tab_changed", self.on_tab_changed)
    
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
    
    def on_tab_changed(self, tab_name):
        """Handle tab changes to update content as needed"""
        print(f"Switched to {tab_name} tab")
        
        # Refresh tab content as needed
        if tab_name == "Temperature Trends":
            self.temp_graph.update_city_list()
        elif tab_name == "City Comparison":
            # Anything that needs refreshing in comparison tab
            pass
    
    def start(self):
        """Start the application window"""
        self.window.run()
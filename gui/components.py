# gui/components.py
import tkinter as tk
from tkinter import ttk, messagebox

class SearchBar:
    """Search bar for city input"""
    
    def __init__(self, parent, on_search):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.X, pady=10)
        
        self.label = ttk.Label(self.frame, text="Enter city:")
        self.label.pack(side=tk.LEFT, padx=5)
        
        self.entry = ttk.Entry(self.frame, width=30)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", lambda e: on_search(self.entry.get()))
        
        self.button = ttk.Button(self.frame, text="Search", 
                               command=lambda: on_search(self.entry.get()))
        self.button.pack(side=tk.LEFT, padx=5)

class WeatherDisplay:
    """Display for current weather"""
    
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # City and date header
        self.header = ttk.Label(self.frame, text="Weather Information", 
                              font=("Arial", 16, "bold"))
        self.header.pack(pady=10)
        
        # Weather info
        self.info_frame = ttk.Frame(self.frame)
        self.info_frame.pack(fill=tk.X, pady=5)
        
        # Temperature
        self.temp_label = ttk.Label(self.info_frame, text="Temperature: --°F", 
                                  font=("Arial", 14))
        self.temp_label.pack(pady=5)
        
        # Feels like
        self.feels_label = ttk.Label(self.info_frame, text="Feels like: --°F")
        self.feels_label.pack(pady=2)
        
        # Description
        self.desc_label = ttk.Label(self.info_frame, text="Description: --")
        self.desc_label.pack(pady=2)
        
        # Humidity
        self.humidity_label = ttk.Label(self.info_frame, text="Humidity: --%")
        self.humidity_label.pack(pady=2)
        
        # Wind
        self.wind_label = ttk.Label(self.info_frame, text="Wind: -- mph")
        self.wind_label.pack(pady=2)
    
    def update(self, weather_data):
        """Update the display with weather data"""
        if not weather_data:
            messagebox.showerror("Error", "Failed to get weather data")
            return
            
        self.header.config(text=f"{weather_data['city']}, {weather_data['country']}")
        self.temp_label.config(text=f"Temperature: {weather_data['temperature']}°F")
        self.feels_label.config(text=f"Feels like: {weather_data['feels_like']}°F")
        self.desc_label.config(text=f"Description: {weather_data['description']}")
        self.humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
        self.wind_label.config(text=f"Wind: {weather_data['wind_speed']} mph")
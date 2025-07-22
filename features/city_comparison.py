"""City comparison feature for weather dashboard"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Callable

class CityComparison:
    """Allows comparing weather data between two or more cities"""
    
    def __init__(self, parent, api_callback: Callable, processor_callback: Callable):
        """
        Initialize city comparison feature
        
        Args:
            parent: Parent frame to place the comparison widget
            api_callback: Function to call to fetch weather data
            processor_callback: Function to process API responses
        """
        self.parent = parent
        self.api_callback = api_callback
        self.processor_callback = processor_callback
        self.cities = []  # List to store city data
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the comparison UI widgets"""
        self.frame = ttk.LabelFrame(self.parent, text="City Comparison")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # City entry and add button
        entry_frame = ttk.Frame(self.frame)
        entry_frame.pack(fill=tk.X, pady=5)
        
        self.city_entry = ttk.Entry(entry_frame, width=20)
        self.city_entry.pack(side=tk.LEFT, padx=5)
        self.city_entry.bind("<Return>", lambda e: self.add_city())
        
        add_button = ttk.Button(entry_frame, text="Add City", command=self.add_city)
        add_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(entry_frame, text="Clear All", command=self.clear_cities)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Comparison table
        self.tree = ttk.Treeview(self.frame, columns=("city", "temp", "humidity", "wind"), show="headings")
        self.tree.heading("city", text="City")
        self.tree.heading("temp", text="Temperature (°F)")
        self.tree.heading("humidity", text="Humidity (%)")
        self.tree.heading("wind", text="Wind (mph)")
        
        self.tree.column("city", width=150)
        self.tree.column("temp", width=120)
        self.tree.column("humidity", width=100)
        self.tree.column("wind", width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def add_city(self):
        """Add a city to the comparison table"""
        city = self.city_entry.get().strip()
        
        if not city:
            messagebox.showinfo("Input Required", "Please enter a city name")
            return
        
        # Check if city already in the list
        for existing_city in self.cities:
            if existing_city['city'].lower() == city.lower():
                messagebox.showinfo("Duplicate", f"{city} is already in the comparison")
                return
        
        # Fetch weather data
        try:
            weather_data = self.api_callback(city)
            
            if weather_data:
                # Process the data
                processed_data = self.processor_callback(weather_data)
                
                # Add to cities list
                self.cities.append(processed_data)
                
                # Add to tree view
                self.tree.insert("", tk.END, values=(
                    processed_data['city'],
                    f"{processed_data['temperature']}°F",
                    f"{processed_data['humidity']}%",
                    f"{processed_data['wind_speed']} mph"
                ))
                
                # Clear entry
                self.city_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Could not find weather data for '{city}'")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def clear_cities(self):
        """Clear all cities from the comparison table"""
        self.cities = []
        for item in self.tree.get_children():
            self.tree.delete(item)
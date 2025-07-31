"""Temperature graph visualization feature"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Dict, Any, List, Callable
from datetime import datetime, timedelta
import random  # For demo data only

class TemperatureGraph:
    """Displays temperature trends over time"""
    
    def __init__(self, parent, storage_callback: Callable):
        """
        Initialize temperature graph feature
        
        Args:
            parent: Parent frame to place the graph
            storage_callback: Function to retrieve weather history data
        """
        self.parent = parent
        self.storage_callback = storage_callback
        self.current_city = None
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        """Create the graph UI widgets"""
        self.frame = ttk.LabelFrame(self.parent, text="Temperature Trends")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Controls frame
        controls_frame = ttk.Frame(self.frame)
        controls_frame.pack(fill=tk.X, pady=5)
        
        # City selection
        ttk.Label(controls_frame, text="City:").pack(side=tk.LEFT, padx=5)
        self.city_var = tk.StringVar()
        self.city_combo = ttk.Combobox(controls_frame, textvariable=self.city_var, width=20)
        self.city_combo.pack(side=tk.LEFT, padx=5)
        self.city_combo.bind("<<ComboboxSelected>>", lambda e: self.update_graph())
        
        # Time range selection
        ttk.Label(controls_frame, text="Range:").pack(side=tk.LEFT, padx=(15, 5))
        self.range_var = tk.StringVar(value="7 days")
        range_combo = ttk.Combobox(controls_frame, textvariable=self.range_var, 
                                  values=["7 days", "14 days", "30 days"], width=10)
        range_combo.pack(side=tk.LEFT, padx=5)
        range_combo.bind("<<ComboboxSelected>>", lambda e: self.update_graph())
        
        # Refresh button
        refresh_btn = ttk.Button(controls_frame, text="Refresh", command=self.update_graph)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Create matplotlib figure and canvas
        self.figure, self.ax = plt.subplots(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Initial message
        self.ax.text(0.5, 0.5, "Select a city to view temperature trends", 
                    ha='center', va='center', fontsize=12)
        self.ax.axis('off')
        
        # Update city list
        self.update_city_list()
        
    def update_city_list(self):
        """Update the list of cities in the combobox"""
        try:
            # Get all cities from storage
            history = self.storage_callback()
            cities = list(history.keys()) if history else []
            
            if not cities:
                # Demo data if no cities are available
                cities = ["New York", "London", "Tokyo", "Paris", "Sydney"]
                
            self.city_combo['values'] = cities
            
            # Select first city if available and none is selected
            if cities and not self.city_var.get():
                self.city_var.set(cities[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load city list: {str(e)}")
    
    def update_graph(self):
        """Update the temperature graph based on selected city and time range"""
        city = self.city_var.get()
        
        if not city:
            return
            
        self.current_city = city
        self.ax.clear()
        
        try:
            # Get the selected date range
            range_text = self.range_var.get()
            days = int(range_text.split()[0])  # Extract number from "X days"
            
            # Get weather history from storage
            history = self.storage_callback()
            
            # Check if we have data for this city
            if not history or city not in history or not history[city]:
                # Generate demo data if no real data exists
                self._generate_demo_data(city, days)
                return
                
            # Get data for the selected city
            city_data = history[city]
            
            # Extract dates and temperatures
            dates = []
            temperatures = []
            
            for entry in city_data[-days:]:  # Get last X days
                dates.append(entry.get('date', ''))
                temperatures.append(entry.get('temperature', 0))
            
            # Plot the data
            self.ax.plot(dates, temperatures, 'o-', color='tab:blue', linewidth=2)
            self.ax.set_title(f"Temperature Trends for {city} - Last {days} Days")
            self.ax.set_xlabel("Date")
            self.ax.set_ylabel("Temperature (°F)")
            self.ax.grid(True, linestyle='--', alpha=0.7)
            
            # Format the x-axis to handle date strings better
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Update the canvas
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update graph: {str(e)}")
            print(f"Graph error: {e}")
    
    def _generate_demo_data(self, city, days):
        """Generate demo data for visualization when no real data exists"""
        today = datetime.now()
        dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
        dates.reverse()  # So dates go from oldest to newest
        
        # Generate random temperatures between 50-80°F with some continuity
        temp = 65  # Starting temperature
        temperatures = []
        for _ in range(days):
            # Add some randomness but maintain continuity
            change = random.uniform(-5, 5)
            temp = max(min(temp + change, 85), 45)  # Keep between 45-85°F
            temperatures.append(round(temp, 1))
        
        # Plot the demo data
        self.ax.plot(dates, temperatures, 'o-', color='tab:orange', linewidth=2)
        self.ax.set_title(f"Temperature Trends for {city} - Demo Data")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Temperature (°F)")
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add watermark for demo data
        self.ax.text(0.5, 0.5, "DEMO DATA", 
                    ha='center', va='center', color='red', alpha=0.2,
                    fontsize=40, rotation=30, transform=self.ax.transAxes)
        
        # Format the x-axis
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Update the canvas
        self.canvas.draw()
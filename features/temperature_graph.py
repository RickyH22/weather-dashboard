"""Temperature graph visualization feature"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Dict, Any, List, Callable
from datetime import datetime

class TemperatureGraph:
    """Displays temperature trends over time"""
    
    def __init__(self, parent, api_callback: Callable, storage_callback: Callable = None):
        """
        Initialize temperature graph feature
        
        Args:
            parent: Parent frame to place the graph
            api_callback: Function to fetch historical weather data
            storage_callback: Optional function to retrieve cached weather history
        """
        self.parent = parent
        self.api_callback = api_callback
        self.storage_callback = storage_callback
        self.current_city = None
        self.data_source = tk.StringVar(value="api")  # "api" or "storage"
        
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
        self.city_entry = ttk.Entry(controls_frame, textvariable=self.city_var, width=20)
        self.city_entry.pack(side=tk.LEFT, padx=5)
        self.city_entry.bind("<Return>", lambda e: self.update_graph())
        
        # Time range selection
        ttk.Label(controls_frame, text="Range:").pack(side=tk.LEFT, padx=(15, 5))
        self.range_var = tk.StringVar(value="7")
        range_combo = ttk.Combobox(controls_frame, textvariable=self.range_var, 
                                  values=["5", "7", "14"], width=5)
        range_combo.pack(side=tk.LEFT, padx=5)
        
        # Data source selection (API or Storage)
        data_frame = ttk.Frame(controls_frame)
        data_frame.pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(data_frame, text="Live API Data", 
                       variable=self.data_source, value="api").pack(side=tk.TOP, anchor=tk.W)
        ttk.Radiobutton(data_frame, text="Stored Data", 
                       variable=self.data_source, value="storage").pack(side=tk.TOP, anchor=tk.W)
        
        # Update button
        update_btn = ttk.Button(controls_frame, text="Update Graph", command=self.update_graph)
        update_btn.pack(side=tk.RIGHT, padx=5)
        
        # Create matplotlib figure and canvas
        self.figure, self.ax = plt.subplots(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Initial message
        self.ax.text(0.5, 0.5, "Enter a city and click Update Graph", 
                    ha='center', va='center', fontsize=12)
        self.ax.axis('off')
    
    def update_graph(self):
        """Update the temperature graph with forecast data"""
        city = self.city_var.get().strip()
        
        if not city:
            messagebox.showinfo("Input Required", "Please enter a city name")
            return
            
        self.current_city = city
        self.ax.clear()
        
        try:
            # Show loading message
            self.ax.text(0.5, 0.5, f"Loading forecast for {city}...", 
                        ha='center', va='center', fontsize=12)
            self.canvas.draw()
            
            # Fetch forecast data
            forecast_data = self.api_callback(city)
            
            if not forecast_data or 'daily' not in forecast_data or not forecast_data['daily']:
                self.ax.clear()
                self.ax.text(0.5, 0.5, f"No forecast data available for {city}\nTry a different city name", 
                            ha='center', va='center', fontsize=12)
                self.canvas.draw()
                return
                
            daily_data = forecast_data['daily']
            
            # Extract data for plotting
            dates = []
            max_temps = []
            min_temps = []
            
            for day in daily_data:
                # Format date
                timestamp = day['dt']
                date_obj = datetime.fromtimestamp(timestamp)
                dates.append(date_obj.strftime('%a\n%m/%d'))
                
                # Extract temperatures
                max_temps.append(round(day['temp']['max']))
                min_temps.append(round(day['temp']['min']))
            
            # Clear the loading message and create the plot
            self.ax.clear()
            
            x_positions = range(len(dates))
            
            # Plot max and min temperatures
            self.ax.plot(x_positions, max_temps, 'o-', 
                        color='#FF6B35', linewidth=3, 
                        markersize=8, label='High')
            self.ax.plot(x_positions, min_temps, 'o-', 
                        color='#004E89', linewidth=3, 
                        markersize=8, label='Low')
            
            # Add temperature labels
            for i, (max_temp, min_temp) in enumerate(zip(max_temps, min_temps)):
                self.ax.annotate(f'{max_temp}°', 
                               xy=(i, max_temp), 
                               xytext=(0, 10), 
                               textcoords='offset points',
                               ha='center', va='bottom',
                               fontweight='bold', fontsize=9)
                self.ax.annotate(f'{min_temp}°', 
                               xy=(i, min_temp), 
                               xytext=(0, -15), 
                               textcoords='offset points',
                               ha='center', va='top',
                               fontweight='bold', fontsize=9)
            
            # Customize the plot
            self.ax.set_title(f"5-Day Forecast for {city.title()}", fontsize=14, fontweight='bold')
            self.ax.set_xlabel("Date", fontsize=12)
            self.ax.set_ylabel("Temperature (°F)", fontsize=12)
            self.ax.set_xticks(x_positions)
            self.ax.set_xticklabels(dates)
            self.ax.grid(True, linestyle='--', alpha=0.3)
            self.ax.legend(loc='upper right')
            
            # Set y-axis limits
            all_temps = max_temps + min_temps
            if all_temps:
                temp_range = max(all_temps) - min(all_temps)
                padding = max(temp_range * 0.1, 5)
                self.ax.set_ylim(min(all_temps) - padding, max(all_temps) + padding)
            
            plt.tight_layout()
            self.canvas.draw()
            
            print(f"Successfully displayed forecast for {city}")
            
        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Error loading forecast for {city}\n{str(e)}", 
                        ha='center', va='center', fontsize=12)
            self.canvas.draw()
            print(f"Forecast error: {e}")
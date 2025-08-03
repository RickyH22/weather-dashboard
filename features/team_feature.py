"""Team city comparison feature for Weather Dashboard"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
import glob
from typing import List, Dict
import numpy as np

class TeamFeature:
    """Compares weather data from team members' CSV files"""
    
    def __init__(self, parent):
        """
        Initialize team feature
        
        Args:
            parent: Parent frame to place the team widget
        """
        self.parent = parent
        self.csv_files = []
        self.data_frames = {}
        self.current_metric = "Temperature_F"
        
        # Create widgets
        self.create_widgets()
        
        # Auto-load and display all CSV files
        self.auto_load_and_display()
    
    def create_widgets(self):
        """Create the team UI widgets"""
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with title
        header = ttk.Frame(self.frame)
        header.pack(fill=tk.X, pady=(0, 10))
        
        title = ttk.Label(
            header, 
            text="Team Weather Data Comparison", 
            font=("Arial", 16, "bold")
        )
        title.pack(side=tk.LEFT)
        
        # Status label
        self.status_var = tk.StringVar(value="Loading team data...")
        status_label = ttk.Label(header, textvariable=self.status_var, font=("Arial", 10))
        status_label.pack(side=tk.RIGHT)
        
        # Controls area
        controls_frame = ttk.LabelFrame(self.frame, text="Comparison Settings")
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Top row controls
        control_row1 = ttk.Frame(controls_frame)
        control_row1.pack(fill=tk.X, padx=10, pady=5)
        
        # Metric selection
        ttk.Label(control_row1, text="Compare:").pack(side=tk.LEFT, padx=5)
        self.metric_var = tk.StringVar(value=self.current_metric)
        self.metric_combo = ttk.Combobox(
            control_row1, 
            textvariable=self.metric_var,
            values=["Temperature_F", "Humidity", "Wind_Speed"],
            width=15,
            state="readonly"
        )
        self.metric_combo.pack(side=tk.LEFT, padx=5)
        self.metric_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_comparison())
        
        # Chart type selection
        ttk.Label(control_row1, text="Chart Type:").pack(side=tk.LEFT, padx=(15, 5))
        self.chart_type_var = tk.StringVar(value="Bar Chart")
        chart_combo = ttk.Combobox(
            control_row1,
            textvariable=self.chart_type_var,
            values=["Bar Chart", "Line Chart", "Box Plot"],
            width=12,
            state="readonly"
        )
        chart_combo.pack(side=tk.LEFT, padx=5)
        chart_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_comparison())
        
        # Refresh button
        refresh_btn = ttk.Button(
            control_row1, 
            text="🔄 Refresh All", 
            command=self.auto_load_and_display
        )
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Bottom row controls
        control_row2 = ttk.Frame(controls_frame)
        control_row2.pack(fill=tk.X, padx=10, pady=5)
        
        # Load more files button
        load_btn = ttk.Button(
            control_row2, 
            text="📁 Add More Files", 
            command=self.load_additional_csv_files
        )
        load_btn.pack(side=tk.LEFT, padx=5)
        
        # File count display
        self.file_count_var = tk.StringVar(value="No files loaded")
        file_count_label = ttk.Label(control_row2, textvariable=self.file_count_var)
        file_count_label.pack(side=tk.LEFT, padx=15)
        
        # Graph area
        graph_frame = ttk.LabelFrame(self.frame, text="Team Data Comparison")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create matplotlib figure
        self.figure, self.ax = plt.subplots(figsize=(12, 7), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initial message
        self.show_loading_message()
    
    def show_loading_message(self):
        """Show loading message"""
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Loading team weather data...", 
                    ha='center', va='center', fontsize=16)
        self.ax.axis('off')
        self.canvas.draw()
    
    def auto_load_and_display(self):
        """Automatically load all CSV files from data directory and display comparison"""
        # Look for CSV files in the data directory
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        
        if os.path.exists(data_dir):
            csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
        else:
            csv_files = []
        
        # Also check current directory
        current_dir_csvs = glob.glob("*.csv")
        csv_files.extend(current_dir_csvs)
        
        # Remove duplicates
        self.csv_files = list(set(csv_files))
        
        if self.csv_files:
            self.load_data_frames()
            self.refresh_comparison()
        else:
            self.show_no_files_message()
    
    def show_no_files_message(self):
        """Show message when no CSV files are found"""
        self.ax.clear()
        self.ax.text(0.5, 0.6, "No CSV files found in data directory", 
                    ha='center', va='center', fontsize=16, fontweight='bold')
        self.ax.text(0.5, 0.4, "Click 'Add More Files' to select CSV files manually", 
                    ha='center', va='center', fontsize=12)
        self.ax.axis('off')
        self.canvas.draw()
        self.status_var.set("No files found")
        self.file_count_var.set("0 files loaded")
    
    def load_additional_csv_files(self):
        """Load additional CSV files through file dialog"""
        files = filedialog.askopenfilenames(
            title="Select Additional CSV Files",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        
        if files:
            # Add to existing files (avoid duplicates)
            for file in files:
                if file not in self.csv_files:
                    self.csv_files.append(file)
            
            self.load_data_frames()
            self.refresh_comparison()
    
    def load_data_frames(self):
        """Load data from all CSV files into pandas DataFrames"""
        self.data_frames = {}
        failed_files = []
        successful_files = []
        
        for file_path in self.csv_files:
            try:
                # Extract filename as identifier
                file_name = os.path.basename(file_path).replace('.csv', '')
                
                # Read the file, handling various comment formats
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Skip comment lines and empty lines
                cleaned_lines = []
                for line in lines:
                    stripped = line.strip()
                    if stripped and not stripped.startswith('//') and not stripped.startswith('#'):
                        cleaned_lines.append(line)
                
                if not cleaned_lines:
                    failed_files.append(f"{file_name} (empty file)")
                    continue
                
                # Create DataFrame from cleaned data
                from io import StringIO
                cleaned_data = StringIO(''.join(cleaned_lines))
                df = pd.read_csv(cleaned_data)
                
                # Clean column names
                df.columns = [col.strip() for col in df.columns]
                
                # Check for required columns
                required_cols = ['Date', 'City']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    failed_files.append(f"{file_name} (missing: {', '.join(missing_cols)})")
                    continue
                
                # Fix common typos in column names
                if 'Temerature_F' in df.columns and 'Temperature_F' not in df.columns:
                    df.rename(columns={'Temerature_F': 'Temperature_F'}, inplace=True)
                
                # Store the DataFrame
                self.data_frames[file_name] = df
                successful_files.append(file_name)
                
            except Exception as e:
                failed_files.append(f"{os.path.basename(file_path)} ({str(e)[:50]}...)")
        
        # Update status
        success_count = len(successful_files)
        total_count = len(self.csv_files)
        
        self.file_count_var.set(f"{success_count} of {total_count} files loaded successfully")
        
        if successful_files:
            self.status_var.set(f"Loaded: {', '.join(successful_files)}")
        else:
            self.status_var.set("No files loaded successfully")
        
        # Show warnings for failed files
        if failed_files:
            warning_msg = f"Issues with {len(failed_files)} files:\n" + "\n".join(failed_files[:5])
            if len(failed_files) > 5:
                warning_msg += f"\n... and {len(failed_files) - 5} more"
            messagebox.showwarning("File Loading Issues", warning_msg)
    
    def refresh_comparison(self):
        """Refresh the comparison visualization"""
        if not self.data_frames:
            self.show_no_files_message()
            return
        
        # Get current settings
        self.current_metric = self.metric_var.get()
        chart_type = self.chart_type_var.get()
        
        # Clear previous plot
        self.ax.clear()
        
        # Collect data for comparison
        comparison_data = self.prepare_comparison_data()
        
        if not comparison_data:
            self.ax.text(0.5, 0.5, f"No {self.current_metric} data found in loaded files", 
                        ha='center', va='center', fontsize=14)
            self.ax.axis('off')
            self.canvas.draw()
            return
        
        # Create the appropriate chart
        if chart_type == "Bar Chart":
            self.create_bar_chart(comparison_data)
        elif chart_type == "Line Chart":
            self.create_line_chart(comparison_data)
        elif chart_type == "Box Plot":
            self.create_box_plot(comparison_data)
        
        self.canvas.draw()
    
    def prepare_comparison_data(self):
        """Prepare data for comparison visualization"""
        comparison_data = {}
        
        for file_name, df in self.data_frames.items():
            if self.current_metric not in df.columns:
                continue
            
            # Group by city and calculate averages
            for city in df['City'].unique():
                city_data = df[df['City'] == city]
                metric_values = city_data[self.current_metric].dropna()
                
                if len(metric_values) > 0:
                    city_key = f"{city}"
                    if city_key not in comparison_data:
                        comparison_data[city_key] = []
                    
                    # Add all values for this city from this file
                    comparison_data[city_key].extend(metric_values.tolist())
        
        return comparison_data
    
    def create_bar_chart(self, data):
        """Create a bar chart comparison"""
        cities = list(data.keys())
        avg_values = [np.mean(values) for values in data.values()]
        
        bars = self.ax.bar(cities, avg_values, color='skyblue', alpha=0.8, edgecolor='navy')
        
        # Add value labels on bars
        for bar, value in zip(bars, avg_values):
            height = bar.get_height()
            self.ax.annotate(f'{value:.1f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom', fontweight='bold')
        
        self.ax.set_title(f'Average {self.current_metric} by City (All Team Files)', 
                         fontsize=14, fontweight='bold')
        self.ax.set_ylabel(self.get_metric_label())
        self.ax.set_xlabel('Cities')
        plt.xticks(rotation=45, ha='right')
        self.ax.grid(True, alpha=0.3)
        plt.tight_layout()
    
    def create_line_chart(self, data):
        """Create a line chart comparison"""
        cities = list(data.keys())
        avg_values = [np.mean(values) for values in data.values()]
        
        self.ax.plot(cities, avg_values, 'o-', linewidth=2, markersize=8, color='darkblue')
        
        # Add value labels
        for i, (city, value) in enumerate(zip(cities, avg_values)):
            self.ax.annotate(f'{value:.1f}',
                           xy=(i, value),
                           xytext=(0, 10),
                           textcoords="offset points",
                           ha='center', va='bottom', fontweight='bold')
        
        self.ax.set_title(f'{self.current_metric} Trends Across Cities (All Team Files)', 
                         fontsize=14, fontweight='bold')
        self.ax.set_ylabel(self.get_metric_label())
        self.ax.set_xlabel('Cities')
        plt.xticks(rotation=45, ha='right')
        self.ax.grid(True, alpha=0.3)
        plt.tight_layout()
    
    def create_box_plot(self, data):
        """Create a box plot comparison"""
        cities = list(data.keys())
        values = [data[city] for city in cities]
        
        box_plot = self.ax.boxplot(values, labels=cities, patch_artist=True)
        
        # Color the boxes
        colors = plt.cm.Set3(np.linspace(0, 1, len(cities)))
        for patch, color in zip(box_plot['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
        
        self.ax.set_title(f'{self.current_metric} Distribution by City (All Team Files)', 
                         fontsize=14, fontweight='bold')
        self.ax.set_ylabel(self.get_metric_label())
        self.ax.set_xlabel('Cities')
        plt.xticks(rotation=45, ha='right')
        self.ax.grid(True, alpha=0.3)
        plt.tight_layout()
    
    def get_metric_label(self):
        """Get the appropriate label for the current metric"""
        labels = {
            'Temperature_F': 'Temperature (°F)',
            'Humidity': 'Humidity (%)',
            'Wind_Speed': 'Wind Speed (mph)'
        }
        return labels.get(self.current_metric, self.current_metric)
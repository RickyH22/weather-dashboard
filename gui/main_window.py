# gui/main_window.py
"""Main application window"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict

class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather Dashboard")
        self.root.geometry("900x700")
        
        # Callbacks storage
        self.callbacks: Dict[str, Callable] = {}
        
        # Create header frame (will contain search and theme controls)
        self.header_frame = ttk.Frame(self.root, padding="10")
        self.header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Create main content area with notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs for each feature
        self.content_frame = ttk.Frame(self.notebook, padding="10")
        self.features_frame = ttk.Frame(self.notebook, padding="10")
        self.graphs_frame = ttk.Frame(self.notebook, padding="10")
        self.settings_frame = ttk.Frame(self.notebook, padding="10")
        
        # Add the frames as tabs
        self.notebook.add(self.content_frame, text="Current Weather")
        self.notebook.add(self.features_frame, text="City Comparison")
        self.notebook.add(self.graphs_frame, text="Temperature Trends")
        self.notebook.add(self.settings_frame, text="Settings")
        
        # Style the tabs to make them bigger and centered
        self.style = ttk.Style()
        
        # Make tabs larger with more padding
        self.style.configure("TNotebook.Tab", padding=[20, 10], font=('Arial', 12))
        
        # Center the tabs
        self.style.configure("TNotebook", tabposition='n')
        
        # Add some margin around the notebook to center tabs
        self.notebook.pack_propagate(0)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        
    def register_callback(self, event: str, callback: Callable):
        """Register event callbacks"""
        self.callbacks[event] = callback
    
    def trigger_callback(self, event: str, *args, **kwargs):
        """Trigger a registered callback"""
        if event in self.callbacks:
            return self.callbacks[event](*args, **kwargs)
    
    def _on_tab_changed(self, event):
        """Handle tab change event"""
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        self.trigger_callback("tab_changed", current_tab)
    
    def run(self):
        """Start the main event loop"""
        self.root.mainloop()

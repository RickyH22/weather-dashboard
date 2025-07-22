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
        self.root.geometry("800x600")
        
        # Callbacks storage
        self.callbacks: Dict[str, Callable] = {}
        
        # Create frames
        self.header_frame = ttk.Frame(self.root, padding="10")
        self.header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.content_frame = ttk.Frame(self.root, padding="10")
        self.content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add features frame
        self.features_frame = ttk.Frame(self.root, padding="10")
        self.features_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)  # Give weight to features frame
    
    def register_callback(self, event: str, callback: Callable):
        """Register event callbacks"""
        self.callbacks[event] = callback
    
    def trigger_callback(self, event: str, *args, **kwargs):
        """Trigger a registered callback"""
        if event in self.callbacks:
            return self.callbacks[event](*args, **kwargs)
    
    def run(self):
        """Start the main event loop"""
        self.root.mainloop()

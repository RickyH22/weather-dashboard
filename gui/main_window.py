# gui/main_window.py
"""Main application window"""

import tkinter as tk
from typing import Callable, Dict

class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather Dashboard")
        self.root.geometry("800x600")
        
        # Callbacks storage
        self.callbacks: Dict[str, Callable] = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize UI components"""
        # Create frames
        self.header_frame = tk.Frame(self.root, bg='#2196F3', height=100)
        self.header_frame.pack(fill=tk.X)
        
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.feature_frame = tk.Frame(self.root)
        self.feature_frame.pack(fill=tk.X, padx=20, pady=10)
    
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

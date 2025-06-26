# features/history.py
"""Weather history feature"""

import tkinter as tk
from .base import Feature

class HistoryFeature(Feature):
    """Display weather history"""
    
    def get_name(self) -> str:
        return "Weather History"
    
    def initialize(self, parent_frame: tk.Frame) -> None:
        """Create history UI"""
        self.frame = tk.Frame(parent_frame)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create history listbox
        self.history_listbox = tk.Listbox(self.frame)
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Load existing history
        self.refresh_history()
    
    def update(self, weather_data: dict) -> None:
        """Update history when new weather is fetched"""
        self.refresh_history()
    
    def refresh_history(self):
        """Refresh history display"""
        self.history_listbox.delete(0, tk.END)
        
        history = self.storage.load_history()
        for entry in history:
            display_text = f"{entry['timestamp'][:10]} - {entry['city']}: {entry['temperature']}°F"
            self.history_listbox.insert(tk.END, display_text)

"""Theme switcher feature for weather dashboard"""

import tkinter as tk
from tkinter import ttk
import datetime

class ThemeSwitcher:
    """Allows switching between light and dark themes"""
    
    def __init__(self, parent, root):
        """
        Initialize theme switcher
        
        Args:
            parent: Parent frame for the switcher controls
            root: Root window to apply themes to
        """
        self.parent = parent
        self.root = root
        
        # Define color schemes
        self.themes = {
            "light": {
                "bg": "#f0f0f0",
                "fg": "#333333",
                "accent": "#0078d7",
                "highlight": "#e5f1fb",
                "secondary": "#d0d0d0",
                "text": "black"
            },
            "dark": {
                "bg": "#2d2d2d",
                "fg": "#e0e0e0",
                "accent": "#1e90ff",
                "highlight": "#3d3d3d",
                "secondary": "#555555",
                "text": "white"
            }
        }
        
        self.current_theme = "light"
        self.create_widgets()
        
        # Check time of day for auto theme
        self.check_auto_theme()
    
    def create_widgets(self):
        """Create the theme switcher UI"""
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.X, pady=5)
        
        # Theme selection
        self.theme_var = tk.StringVar(value="light")
        
        # Create a better looking theme switcher with icons
        self.theme_frame = ttk.LabelFrame(self.frame, text="Theme")
        self.theme_frame.pack(side=tk.RIGHT, padx=10)
        
        # Light theme button
        self.light_btn = ttk.Radiobutton(
            self.theme_frame, 
            text="☀️ Light",
            variable=self.theme_var,
            value="light",
            command=lambda: self.set_theme("light")
        )
        self.light_btn.pack(side=tk.LEFT, padx=5)
        
        # Dark theme button
        self.dark_btn = ttk.Radiobutton(
            self.theme_frame, 
            text="🌙 Dark",
            variable=self.theme_var,
            value="dark",
            command=lambda: self.set_theme("dark")
        )
        self.dark_btn.pack(side=tk.LEFT, padx=5)
        
        # Auto theme button
        self.auto_btn = ttk.Radiobutton(
            self.theme_frame, 
            text="🔄 Auto",
            variable=self.theme_var,
            value="auto",
            command=self.check_auto_theme
        )
        self.auto_btn.pack(side=tk.LEFT, padx=5)
    
    def set_theme(self, theme_name):
        """Set the application theme"""
        if theme_name not in self.themes:
            return
            
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        
        # Configure ttk styles
        style = ttk.Style()
        
        # Configure the main ttk elements
        style.configure("TFrame", background=theme["bg"])
        style.configure("TLabel", background=theme["bg"], foreground=theme["text"])
        style.configure("TButton", background=theme["secondary"], foreground=theme["text"])
        style.configure("TEntry", fieldbackground=theme["secondary"])
        
        # Configure TLabelframe
        style.configure("TLabelframe", background=theme["bg"], foreground=theme["text"])
        style.configure("TLabelframe.Label", background=theme["bg"], foreground=theme["text"])
        
        # Configure other elements
        style.configure("TRadiobutton", background=theme["bg"], foreground=theme["text"])
        style.configure("TCheckbutton", background=theme["bg"], foreground=theme["text"])
        style.configure("TCombobox", fieldbackground=theme["secondary"])
        style.map("TCombobox", fieldbackground=[("readonly", theme["secondary"])])
        
        # Configure Treeview
        style.configure("Treeview", 
                       background=theme["bg"], 
                       fieldbackground=theme["bg"], 
                       foreground=theme["text"])
        style.configure("Treeview.Heading", 
                       background=theme["secondary"], 
                       foreground=theme["text"])
        
        # Apply to standard tk widgets through root
        self.root.configure(bg=theme["bg"])
        
        # Update all frames recursively
        self._update_widget_colors(self.root, theme)
        
    def _update_widget_colors(self, widget, theme):
        """Recursively update colors for all widgets"""
        widget_type = widget.winfo_class()
        
        # Handle specific widget types
        if widget_type in ('Frame', 'Labelframe', 'Toplevel'):
            widget.configure(bg=theme["bg"])
        elif widget_type == 'Label':
            widget.configure(bg=theme["bg"], fg=theme["text"])
        elif widget_type == 'Button':
            widget.configure(bg=theme["secondary"], fg=theme["text"], 
                           activebackground=theme["accent"])
        elif widget_type == 'Listbox':
            widget.configure(bg=theme["secondary"], fg=theme["text"])
        elif widget_type == 'Entry':
            widget.configure(bg=theme["secondary"], fg=theme["text"],
                           insertbackground=theme["text"])
        elif widget_type == 'Canvas':
            widget.configure(bg=theme["bg"])
        
        # Update children
        for child in widget.winfo_children():
            self._update_widget_colors(child, theme)
    
    def check_auto_theme(self):
        """Set theme based on time of day if auto is selected"""
        if self.theme_var.get() == "auto":
            # Get current hour
            hour = datetime.datetime.now().hour
            
            # 6 AM to 6 PM is light theme, otherwise dark
            if 6 <= hour < 18:
                self.set_theme("light")
            else:
                self.set_theme("dark")
                
            # Schedule next check in 15 minutes
            self.root.after(15 * 60 * 1000, self.check_auto_theme)
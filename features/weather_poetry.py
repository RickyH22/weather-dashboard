"""Weather poetry feature that generates poems based on weather conditions"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import random
from typing import Dict, Any, Callable

class WeatherPoetry:
    """Generates poems based on current weather conditions"""
    
    def __init__(self, parent, api_callback: Callable):
        """
        Initialize weather poetry feature
        
        Args:
            parent: Parent frame for the poetry widget
            api_callback: Function to call to fetch current weather data
        """
        self.parent = parent
        self.api_callback = api_callback
        self.current_city = None
        self.current_weather = None
        
        # Poetry templates based on weather conditions
        self.poetry_templates = {
            "clear": [
                "Blue skies over {city},\nSunlight dancing everywhere.\nA perfect day shines.",
                "The sun in {city},\nCasts its golden light today.\nWarmth upon my face.",
                "{city} bathes in light,\nNot a cloud to block the sun.\nPure tranquility."
            ],
            "clouds": [
                "Gray clouds drift above,\n{city}'s sky a canvas.\nNature's art display.",
                "Clouds hang over {city},\nSoft cotton in the blue sky.\nGentle shade below.",
                "Cloudy {city} day,\nThe sun plays hide and seek now.\nPatience brings its light."
            ],
            "rain": [
                "Rain falls in {city},\nDrums a rhythm on rooftops.\nEarth drinks thirstily.",
                "Droplets from the sky,\n{city} shines with wetness now.\nUmbrellas bloom wide.",
                "The rain in {city},\nWashes streets and feeds the trees.\nLife's cycle renewed."
            ],
            "snow": [
                "White blanket descends,\n{city} transformed by snowfall.\nSilent wonderland.",
                "Snowflakes dance and twirl,\n{city} dressed in winter white.\nFootprints tell our tale.",
                "The snow in {city},\nCrystal magic from the sky.\nTime seems to stand still."
            ],
            "thunderstorm": [
                "Thunder cracks the sky,\n{city} trembles at its voice.\nPower unleashed now.",
                "Lightning splits the clouds,\n{city}'s sky electric blue.\nNature's mighty show.",
                "Storm rages above,\n{city} waits for calm again.\nPatience through the dark."
            ],
            "mist": [
                "Misty {city} views,\nThe world wrapped in mystery.\nSoft edges surround.",
                "Fog embraces {city},\nShrouded in a gentle veil.\nSecrets hide within.",
                "Through the mist I see,\n{city}'s outline softened now.\nDreamy atmosphere."
            ],
            "default": [
                "The weather shifts and turns,\n{city} feels nature's changing moods.\nBeauty in each phase.",
                "Whatever skies bring,\n{city} stands beneath it all.\nWeather comes and goes.",
                "In fair or foul weather,\n{city} shows its character.\nBeauty never fades."
            ]
        }
        
        # Create the UI elements
        self.create_widgets()
    
    def create_widgets(self):
        """Create the poetry UI widgets"""
        self.frame = ttk.LabelFrame(self.parent, text="Weather Poetry")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top controls
        controls_frame = ttk.Frame(self.frame)
        controls_frame.pack(fill=tk.X, pady=5)
        
        # City entry
        ttk.Label(controls_frame, text="City:").pack(side=tk.LEFT, padx=5)
        self.city_var = tk.StringVar()
        self.city_entry = ttk.Entry(controls_frame, textvariable=self.city_var, width=20)
        self.city_entry.pack(side=tk.LEFT, padx=5)
        self.city_entry.bind("<Return>", lambda e: self.generate_poem())
        
        # Generate button
        generate_btn = ttk.Button(
            controls_frame, 
            text="✨ Generate Poem", 
            command=self.generate_poem
        )
        generate_btn.pack(side=tk.RIGHT, padx=5)
        
        # Refresh button
        refresh_btn = ttk.Button(
            controls_frame, 
            text="🔄 New Poem", 
            command=lambda: self.generate_poem(refresh=True)
        )
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Poetry display
        poetry_frame = ttk.Frame(self.frame)
        poetry_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Weather icon and condition
        self.weather_var = tk.StringVar(value="Enter a city to get started")
        weather_label = ttk.Label(poetry_frame, textvariable=self.weather_var)
        weather_label.pack(pady=5)
        
        # Poetry text
        self.poetry_text = scrolledtext.ScrolledText(
            poetry_frame, 
            wrap=tk.WORD, 
            width=40, 
            height=10, 
            font=("Georgia", 12)
        )
        self.poetry_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.poetry_text.insert(tk.END, "Your weather-inspired poem will appear here...")
        self.poetry_text.config(state=tk.DISABLED)
    
    def generate_poem(self, refresh=False):
        """Generate a poem based on current weather conditions"""
        city = self.city_var.get().strip()
        
        if not city:
            self.poetry_text.config(state=tk.NORMAL)
            self.poetry_text.delete(1.0, tk.END)
            self.poetry_text.insert(tk.END, "Please enter a city name first.")
            self.poetry_text.config(state=tk.DISABLED)
            return
        
        # Only fetch new weather if city changed or refresh requested
        if city != self.current_city or refresh or not self.current_weather:
            try:
                # Fetch current weather
                weather_data = self.api_callback(city)
                
                if not weather_data:
                    self.poetry_text.config(state=tk.NORMAL)
                    self.poetry_text.delete(1.0, tk.END)
                    self.poetry_text.insert(tk.END, f"Could not retrieve weather data for {city}.")
                    self.poetry_text.config(state=tk.DISABLED)
                    return
                
                self.current_city = city
                self.current_weather = weather_data
                
            except Exception as e:
                self.poetry_text.config(state=tk.NORMAL)
                self.poetry_text.delete(1.0, tk.END)
                self.poetry_text.insert(tk.END, f"Error fetching weather: {str(e)}")
                self.poetry_text.config(state=tk.DISABLED)
                return
        
        # Get the weather condition
        try:
            weather_description = self.current_weather["weather"][0]["main"].lower()
            detailed_description = self.current_weather["weather"][0]["description"]
            temperature = round(self.current_weather["main"]["temp"])
            
            # Update weather display
            self.weather_var.set(f"Current weather in {city}: {detailed_description}, {temperature}°F")
            
            # Map weather to poem template category
            category = "default"
            if "clear" in weather_description:
                category = "clear"
            elif "cloud" in weather_description:
                category = "clouds"
            elif "rain" in weather_description or "drizzle" in weather_description:
                category = "rain"
            elif "snow" in weather_description:
                category = "snow"
            elif "thunder" in weather_description or "storm" in weather_description:
                category = "thunderstorm"
            elif "mist" in weather_description or "fog" in weather_description:
                category = "mist"
            
            # Select a random poem from the appropriate templates
            templates = self.poetry_templates.get(category, self.poetry_templates["default"])
            poem = random.choice(templates).format(city=city)
            
            # Add a temperature-related line
            if temperature > 80:
                temp_line = f"Heat embraces all.\n({temperature}°F)"
            elif temperature > 65:
                temp_line = f"Warmth caresses skin.\n({temperature}°F)"
            elif temperature > 50:
                temp_line = f"Mild air surrounds us.\n({temperature}°F)"
            elif temperature > 32:
                temp_line = f"Coolness in the air.\n({temperature}°F)"
            else:
                temp_line = f"Winter's chill bites deep.\n({temperature}°F)"
            
            # Add the temperature line to the poem
            poem = f"{poem}\n{temp_line}"
            
            # Display the poem
            self.poetry_text.config(state=tk.NORMAL)
            self.poetry_text.delete(1.0, tk.END)
            self.poetry_text.insert(tk.END, poem)
            self.poetry_text.tag_configure("center", justify="center")
            self.poetry_text.tag_add("center", 1.0, tk.END)
            self.poetry_text.config(state=tk.DISABLED)
            
        except Exception as e:
            self.poetry_text.config(state=tk.NORMAL)
            self.poetry_text.delete(1.0, tk.END)
            self.poetry_text.insert(tk.END, f"Error generating poem: {str(e)}")
            self.poetry_text.config(state=tk.DISABLED)
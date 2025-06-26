# core/api.py
"""Weather API client module"""

import requests
from typing import Dict, Optional

class WeatherAPI:
    """Handles all weather API communications"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.timeout = 10
    
    def fetch_weather(self, city: str) -> Optional[Dict]:
        """
        Fetch weather data for a city
        
        Args:
            city: Name of the city
            
        Returns:
            Dictionary with weather data or None if error
        """
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'imperial'
            }
            response = requests.get(
                self.base_url, 
                params=params, 
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API Error: {e}")
            return None

# core/api.py
"""Weather API client module"""

import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()  # Load environment variables
print("API key:", os.getenv("OPENWEATHERMAP_API_KEY"))

class WeatherAPI:
    """Handles all weather API communications"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found in environment variables")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.timeout = 10
    
    def fetch_weather(self, city: str) -> Dict[str, Any]:
        """
        Fetch current weather for a city
        
        Args:
            city: City name to get weather for
            
        Returns:
            Weather data dictionary or None on error
        """
        if not city:
            return None
        
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'imperial'  # For Fahrenheit
        }
        
        try:
            print(f"Sending request to API for city: {city}")
            print(f"API URL: {self.base_url}")
            print(f"Params: {params}")  # Don't print the actual API key in production
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout
            )
            
            print(f"Response status code: {response.status_code}")
            if response.status_code != 200:
                print(f"Error response: {response.text}")
            
            # Handle HTTP errors
            response.raise_for_status()
            
            # Return the parsed JSON data
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print(f"City '{city}' not found")
            else:
                print(f"HTTP error: {e}")
            return None
        except requests.exceptions.ConnectionError:
            print("Network connection error. Please check your internet connection.")
            return None
        except requests.exceptions.Timeout:
            print(f"Request timed out after {self.timeout} seconds")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching weather: {e}")
            return None

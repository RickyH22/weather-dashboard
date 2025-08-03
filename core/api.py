# core/api.py
"""Weather API client module"""

import os
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv
from datetime import datetime

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
    
    def fetch_historical_weather(self, city: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Fetch historical weather data for a city
        
        Args:
            city: City name to get history for
            days: Number of days of history to get
            
        Returns:
            List of daily weather data points
        """
        # Since OpenWeatherMap's historical API requires paid subscription,
        # we'll use the 5-day/3-hour forecast API which is free
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'imperial',  # For Fahrenheit
            'cnt': days * 8  # Get data points for requested days (8 points per day)
        }
        
        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params=params,
                timeout=self.timeout
            )
            
            # Handle HTTP errors
            response.raise_for_status()
            
            # Process the data to get daily readings
            data = response.json()
            
            if 'list' not in data:
                print("Invalid response format")
                return []
                
            # Extract daily data (take first reading of each day)
            daily_data = []
            days_added = set()
            
            for item in data['list']:
                # Convert timestamp to date string
                timestamp = item['dt']
                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                
                # Only take first reading for each day
                if date in days_added:
                    continue
                    
                days_added.add(date)
                
                # Add the data point
                daily_data.append({
                    'date': date,
                    'temperature': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'],
                    'wind_speed': item['wind']['speed']
                })
                
                # Stop once we have enough days
                if len(daily_data) >= days:
                    break
                    
            return daily_data
            
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return []
    
    def fetch_forecast(self, city: str) -> Dict[str, Any]:
        """
        Fetch 7-day weather forecast for a city
        
        Args:
            city: City name to get forecast for
            
        Returns:
            Dictionary with forecast data
        """
        try:
            # Use the 5-day/3-hour forecast API (free tier)
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'imperial'  # For Fahrenheit
            }
            
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params=params,
                timeout=self.timeout
            )
            
            # Handle HTTP errors
            response.raise_for_status()
            
            # Process the data
            data = response.json()
            
            if 'list' not in data:
                print("Invalid response format")
                return {}
            
            # Convert the 3-hour forecasts into daily forecasts
            daily_forecasts = self._process_forecast_data(data['list'])
            
            return {
                'city': data.get('city', {}),
                'daily': daily_forecasts
            }
            
        except requests.exceptions.RequestException as e:
            print(f"API request error for {city}: {e}")
            return {}
        except Exception as e:
            print(f"Error fetching forecast for {city}: {e}")
            return {}

    def _process_forecast_data(self, forecast_list: List[Dict]) -> List[Dict]:
        """
        Process 3-hour forecast data into daily forecasts
        
        Args:
            forecast_list: List of 3-hour forecast data points
            
        Returns:
            List of daily forecast dictionaries
        """
        daily_data = {}
        
        for item in forecast_list:
            # Get the date for this forecast item
            timestamp = item['dt']
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            
            if date not in daily_data:
                daily_data[date] = {
                    'dt': timestamp,
                    'temp': {'max': float('-inf'), 'min': float('inf')},
                    'weather': item['weather'],
                    'temps': []  # Store all temps to calculate average
                }
            
            # Update min/max temperatures
            temp = item['main']['temp']
            daily_data[date]['temps'].append(temp)
            daily_data[date]['temp']['max'] = max(daily_data[date]['temp']['max'], temp)
            daily_data[date]['temp']['min'] = min(daily_data[date]['temp']['min'], temp)
        
        # Convert to list and limit to 7 days
        result = []
        for date in sorted(daily_data.keys())[:7]:
            day_data = daily_data[date]
            result.append({
                'dt': day_data['dt'],
                'temp': day_data['temp'],
                'weather': day_data['weather']
            })
        
        return result

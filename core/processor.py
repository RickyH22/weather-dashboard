# core/processor.py
"""Data processing for weather information"""

from typing import Dict, List, Any
from statistics import mean

class DataProcessor:
    """Handles processing and analysis of weather data"""
    
    def process_api_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant weather information from API response
        
        Args:
            response: Raw API response
            
        Returns:
            Dictionary with processed weather information
        """
        try:
            return {
                'temperature': round(response['main']['temp'], 1),
                'feels_like': round(response['main']['feels_like'], 1),
                'humidity': response['main']['humidity'],
                'description': response['weather'][0]['description'],
                'wind_speed': response['wind']['speed'],
                'city': response['name'],
                'country': response['sys']['country']
            }
        except KeyError as e:
            print(f"Error processing API response: Missing key {e}")
            return {}
    
    def calculate_statistics(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate statistics from historical weather data
        
        Args:
            history: List of historical weather data
            
        Returns:
            Dictionary with statistical information
        """
        if not history or len(history) < 2:
            return {'error': 'Not enough data for statistics'}
        
        try:
            temperatures = [entry['temperature'] for entry in history]
            humidities = [entry['humidity'] for entry in history]
            
            return {
                'avg_temp': round(mean(temperatures), 1),
                'min_temp': round(min(temperatures), 1),
                'max_temp': round(max(temperatures), 1),
                'avg_humidity': round(mean(humidities), 1),
                'data_points': len(history)
            }
        except KeyError as e:
            return {'error': f'Missing data in history: {e}'}
        except Exception as e:
            return {'error': f'Error calculating statistics: {e}'}
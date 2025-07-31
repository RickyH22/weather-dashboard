# core/storage.py
"""Storage management for weather data"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class StorageManager:
    """Handles saving and loading weather data"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        """Create storage file if it doesn't exist"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump({}, file)
    
    def save_weather(self, city: str, data: Dict[str, Any]) -> bool:
        """
        Save weather data for a city
        
        Args:
            city: The city name
            data: Weather data to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Add timestamp
            data['timestamp'] = datetime.now().isoformat()
            
            # Load existing data
            with open(self.filename, 'r') as file:
                all_data = json.load(file)
            
            # Add or update city data
            if city not in all_data:
                all_data[city] = []
            
            all_data[city].append(data)
            
            # Save back to file
            with open(self.filename, 'w') as file:
                json.dump(all_data, file, indent=2)
                
            return True
        
        except Exception as e:
            print(f"Error saving weather data: {e}")
            return False
    
    def load_history(self, city: str) -> List[Dict[str, Any]]:
        """
        Get historical weather data for a city
        
        Args:
            city: The city name
            
        Returns:
            List of historical weather data entries
        """
        try:
            with open(self.filename, 'r') as file:
                all_data = json.load(file)
                
            return all_data.get(city, [])
        
        except Exception as e:
            print(f"Error loading weather history: {e}")
            return []
    
    def get_all_weather(self):
        """Get all stored weather data"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    return json.load(file)
            return {}
        except Exception as e:
            print(f"Error retrieving weather data: {e}")
            return {}
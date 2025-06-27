# app.py
"""Main application that uses the core modules"""

import os
from core.api import WeatherAPI
from core.storage import StorageManager
from core.processor import DataProcessor

def main():
    # Step 1: Set up API with your key
    api_key = "fcd917863c4d493d670641fd9c1bb9a7"  # Replace with your actual OpenWeatherMap API key
    api = WeatherAPI(api_key)
    
    # Step 2: Set up storage
    storage = StorageManager("weather_history.json")
    
    # Step 3: Set up data processor
    processor = DataProcessor()
    
    # Step 4: Test the system
    city = "London"
    
    print(f"Fetching weather data for {city}...")
    weather_data = api.fetch_weather(city)
    
    if weather_data:
        # Process the data
        processed_data = processor.process_api_response(weather_data)
        print("\nProcessed weather data:")
        for key, value in processed_data.items():
            print(f"  {key}: {value}")
        
        # Save to storage
        storage.save_weather(city, processed_data)
        print("\nData saved to storage.")
        
        # Load history and calculate statistics
        history = storage.load_history(city)
        if len(history) > 1:
            stats = processor.calculate_statistics(history)
            print("\nWeather statistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
    else:
        print("Failed to fetch weather data.")

if __name__ == "__main__":
    main()
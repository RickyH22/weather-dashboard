# Weather Dashboard
A desktop application that provides real-time weather data visualization with multiple features for weather tracking and analysis.

## ✨ Features
- **Current Weather Display**: Get real-time temperature, humidity, wind speed, and conditions for any city worldwide
- **City Comparison**: Compare weather conditions between multiple cities side-by-side
- **Temperature Trends**: Visualize temperature history with interactive graphs
- **Weather Poetry**: Generate creative poems based on current weather conditions
- **Team City Data**: Import and compare weather data from CSV files across different cities
- **Theme Options**: Toggle between light mode, dark mode, or auto mode that changes based on time of day

## 🚀 Installation

### Prerequisites
- Python 3.8+
- OpenWeatherMap API key

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/weather-dashboard.git
   cd weather-dashboard
   ```

## 📱 Usage
### Current Weather
Enter a city name in the search bar and press Enter or click the Search button to display current weather conditions.

### City Comparison
Navigate to the "City Comparison" tab to add multiple cities and compare their weather data side-by-side.

### Temperature Trends
The "Temperature Trends" tab shows historical temperature data for selected cities.

### Weather Poetry
Get a creative, weather-inspired poem generated based on the current conditions in your selected city.

### Team City Data
Import CSV files with weather data to compare metrics across different cities.

## 🔍 Directory Structure
weather-dashboard/
├── main.py                # Application entry point
├── core/                  # Core functionality
│   ├── api.py             # Weather API integration
│   ├── processor.py       # Data processing
│   └── storage.py         # Data persistence
├── gui/                   # User interface components
├── features/              # Feature implementations
└── data/                  # Data storage directory

## ⚠️ Troubleshooting
Issue	Solution
API Key Issues	Ensure your API key is correctly set in the .env file
Missing Dependencies	Run pip install requests matplotlib pandas python-dotenv pillow
CSV Import Errors	Make sure CSV files use # for comments instead of //

## 👏 Credits
Weather data provided by OpenWeatherMap
Created as part of the Justice Through Code program
Developed by Ricky Hull
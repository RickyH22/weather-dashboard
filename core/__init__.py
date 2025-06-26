# core/__init__.py
"""Core functionality for Weather Dashboard"""

from .api import WeatherAPI
from .storage import StorageManager
from .processor import DataProcessor

__all__ = ['WeatherAPI', 'StorageManager', 'DataProcessor']
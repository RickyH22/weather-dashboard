# features/base.py
"""Base class for all features"""

from abc import ABC, abstractmethod
from typing import Any

class Feature(ABC):
    """Abstract base class for features"""
    
    def __init__(self, core_modules: dict):
        self.api = core_modules.get('api')
        self.storage = core_modules.get('storage')
        self.processor = core_modules.get('processor')
    
    @abstractmethod
    def get_name(self) -> str:
        """Return feature name"""
        pass
    
    @abstractmethod
    def initialize(self, parent_frame: Any) -> None:
        """Initialize feature UI"""
        pass
    
    @abstractmethod
    def update(self, weather_data: dict) -> None:
        """Update feature with new weather data"""
        pass

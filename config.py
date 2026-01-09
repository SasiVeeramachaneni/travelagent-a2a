"""
Configuration settings for the travel agent
"""
import os
from typing import Dict, Any


class Config:
    """Configuration class for the travel agent"""
    
    # Application settings
    APP_NAME = "Travel Agent"
    APP_VERSION = "1.0.0"
    
    # Agent settings
    DEFAULT_BUDGET_LEVEL = "moderate"
    DEFAULT_TRAVELERS = 1
    MIN_TRIP_DURATION = 1
    MAX_TRIP_DURATION = 30
    
    # Currency settings
    DEFAULT_CURRENCY = "$"
    SUPPORTED_CURRENCIES = ["$", "€", "£", "¥", "₹"]
    
    # Conversation settings
    MAX_CONVERSATION_HISTORY = 100
    
    # API settings (Azure OpenAI credentials loaded from .env)
    OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT", "")
    TENANT_ID = os.getenv("TENANT_ID", "")
    CLIENT_ID = os.getenv("CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
    
    # Feature flags
    ENABLE_AI_SERVICE = True  # Enable Azure OpenAI integration
    ENABLE_REAL_TIME_PRICING = False
    ENABLE_BOOKING_INTEGRATION = False
    ENABLE_WEATHER_INTEGRATION = False
    
    # Legacy API settings (for backward compatibility)
    FLIGHT_API_KEY = os.getenv("FLIGHT_API_KEY", "")
    HOTEL_API_KEY = os.getenv("HOTEL_API_KEY", "")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    
    # Cost calculation settings
    MISCELLANEOUS_BUFFER_PERCENTAGE = 0.15  # 15% buffer
    
    # Supported destinations
    SUPPORTED_DESTINATIONS = [
        "Paris", "Tokyo", "New York", "London", "Rome",
        "Barcelona", "Dubai", "Singapore", "Sydney", "Bali"
    ]
    
    # Interest categories
    INTEREST_CATEGORIES = [
        "culture", "adventure", "food", "relaxation",
        "nightlife", "shopping", "nature", "history"
    ]
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """
        Get all configuration as dictionary
        
        Returns:
            Dict: Configuration dictionary
        """
        return {
            'app_name': cls.APP_NAME,
            'app_version': cls.APP_VERSION,
            'default_budget_level': cls.DEFAULT_BUDGET_LEVEL,
            'default_travelers': cls.DEFAULT_TRAVELERS,
            'default_currency': cls.DEFAULT_CURRENCY,
            'supported_destinations': cls.SUPPORTED_DESTINATIONS,
            'interest_categories': cls.INTEREST_CATEGORIES
        }


# Development settings
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


# Production settings
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


# Testing settings
class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


# Configuration mapping
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env: str = 'default') -> Config:
    """
    Get configuration based on environment
    
    Args:
        env: Environment name
        
    Returns:
        Config: Configuration class
    """
    return config_by_name.get(env, DevelopmentConfig)

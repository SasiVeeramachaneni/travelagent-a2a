"""
Weather Knowledge
Contains climate data, seasonal patterns, and packing recommendations
"""
from typing import Dict, List, Optional, Any


class WeatherKnowledge:
    """
    Knowledge base for weather and climate information
    
    This module provides:
    - Monthly temperature and rainfall data
    - Best/worst times to visit
    - Seasonal patterns
    - Packing recommendations
    - Weather-related activities
    """
    
    def __init__(self):
        """Initialize weather knowledge base"""
        self.climate_data = self._load_climate_data()
        self.packing_guides = self._load_packing_guides()
    
    def _load_climate_data(self) -> Dict[str, Any]:
        """
        Load climate database
        
        Structure:
        {
            'destination': {
                'monthly_data': {month: {temp_high, temp_low, rainfall, conditions}},
                'best_months': [months],
                'worst_months': [months],
                'peak_season': str,
                'off_season': str
            }
        }
        """
        return {
            'paris': {
                'monthly_data': {
                    'january': {'temp_high': 7, 'temp_low': 3, 'rainfall': 54, 'conditions': 'Cold, occasional rain'},
                    'february': {'temp_high': 8, 'temp_low': 3, 'rainfall': 44, 'conditions': 'Cold, less rain'},
                    'march': {'temp_high': 12, 'temp_low': 5, 'rainfall': 48, 'conditions': 'Cool, spring begins'},
                    'april': {'temp_high': 16, 'temp_low': 7, 'rainfall': 53, 'conditions': 'Mild, pleasant'},
                    'may': {'temp_high': 20, 'temp_low': 11, 'rainfall': 65, 'conditions': 'Warm, sunny'},
                    'june': {'temp_high': 23, 'temp_low': 14, 'rainfall': 54, 'conditions': 'Warm, perfect weather'},
                    'july': {'temp_high': 25, 'temp_low': 16, 'rainfall': 63, 'conditions': 'Warm, peak summer'},
                    'august': {'temp_high': 25, 'temp_low': 16, 'rainfall': 43, 'conditions': 'Warm, dry'},
                    'september': {'temp_high': 21, 'temp_low': 12, 'rainfall': 54, 'conditions': 'Pleasant, fewer crowds'},
                    'october': {'temp_high': 16, 'temp_low': 9, 'rainfall': 62, 'conditions': 'Cool, autumn colors'},
                    'november': {'temp_high': 10, 'temp_low': 5, 'rainfall': 51, 'conditions': 'Cold, rainy'},
                    'december': {'temp_high': 7, 'temp_low': 3, 'rainfall': 59, 'conditions': 'Cold, festive'}
                },
                'best_months': ['May', 'June', 'September', 'October'],
                'worst_months': ['November', 'December', 'January'],
                'peak_season': 'June-August',
                'off_season': 'November-March'
            },
            'tokyo': {
                'monthly_data': {
                    'january': {'temp_high': 10, 'temp_low': 2, 'rainfall': 52, 'conditions': 'Cold, dry'},
                    'february': {'temp_high': 10, 'temp_low': 2, 'rainfall': 56, 'conditions': 'Cold, dry'},
                    'march': {'temp_high': 13, 'temp_low': 5, 'rainfall': 118, 'conditions': 'Cool, cherry blossoms start'},
                    'april': {'temp_high': 19, 'temp_low': 10, 'rainfall': 125, 'conditions': 'Mild, cherry blossoms peak'},
                    'may': {'temp_high': 23, 'temp_low': 15, 'rainfall': 138, 'conditions': 'Warm, pleasant'},
                    'june': {'temp_high': 25, 'temp_low': 19, 'rainfall': 168, 'conditions': 'Warm, rainy season begins'},
                    'july': {'temp_high': 29, 'temp_low': 23, 'rainfall': 154, 'conditions': 'Hot, humid'},
                    'august': {'temp_high': 31, 'temp_low': 24, 'rainfall': 168, 'conditions': 'Very hot, humid'},
                    'september': {'temp_high': 27, 'temp_low': 21, 'rainfall': 210, 'conditions': 'Warm, typhoon season'},
                    'october': {'temp_high': 21, 'temp_low': 15, 'rainfall': 198, 'conditions': 'Pleasant, autumn colors'},
                    'november': {'temp_high': 16, 'temp_low': 9, 'rainfall': 93, 'conditions': 'Cool, comfortable'},
                    'december': {'temp_high': 12, 'temp_low': 4, 'rainfall': 51, 'conditions': 'Cold, dry'}
                },
                'best_months': ['March', 'April', 'October', 'November'],
                'worst_months': ['July', 'August', 'September'],
                'peak_season': 'March-April (cherry blossoms), October-November (autumn)',
                'off_season': 'December-February, July-August'
            },
            'new york': {
                'monthly_data': {
                    'january': {'temp_high': 3, 'temp_low': -3, 'rainfall': 92, 'conditions': 'Very cold, snow'},
                    'february': {'temp_high': 5, 'temp_low': -2, 'rainfall': 78, 'conditions': 'Cold, snow'},
                    'march': {'temp_high': 10, 'temp_low': 1, 'rainfall': 110, 'conditions': 'Cool, spring arrives'},
                    'april': {'temp_high': 16, 'temp_low': 7, 'rainfall': 114, 'conditions': 'Mild, pleasant'},
                    'may': {'temp_high': 22, 'temp_low': 12, 'rainfall': 106, 'conditions': 'Warm, sunny'},
                    'june': {'temp_high': 27, 'temp_low': 18, 'rainfall': 112, 'conditions': 'Warm, humid'},
                    'july': {'temp_high': 29, 'temp_low': 21, 'rainfall': 116, 'conditions': 'Hot, humid'},
                    'august': {'temp_high': 28, 'temp_low': 20, 'rainfall': 113, 'conditions': 'Hot, humid'},
                    'september': {'temp_high': 24, 'temp_low': 16, 'rainfall': 109, 'conditions': 'Pleasant, comfortable'},
                    'october': {'temp_high': 18, 'temp_low': 10, 'rainfall': 111, 'conditions': 'Cool, beautiful fall'},
                    'november': {'temp_high': 11, 'temp_low': 4, 'rainfall': 102, 'conditions': 'Cold, variable'},
                    'december': {'temp_high': 5, 'temp_low': -1, 'rainfall': 109, 'conditions': 'Very cold, festive'}
                },
                'best_months': ['April', 'May', 'September', 'October'],
                'worst_months': ['January', 'February', 'July', 'August'],
                'peak_season': 'April-June, September-October',
                'off_season': 'January-March'
            },
            'london': {
                'monthly_data': {
                    'january': {'temp_high': 8, 'temp_low': 2, 'rainfall': 55, 'conditions': 'Cold, wet'},
                    'february': {'temp_high': 8, 'temp_low': 2, 'rainfall': 40, 'conditions': 'Cold, drier'},
                    'march': {'temp_high': 11, 'temp_low': 4, 'rainfall': 42, 'conditions': 'Cool, spring begins'},
                    'april': {'temp_high': 14, 'temp_low': 6, 'rainfall': 44, 'conditions': 'Mild, pleasant'},
                    'may': {'temp_high': 17, 'temp_low': 9, 'rainfall': 49, 'conditions': 'Comfortable, sunny spells'},
                    'june': {'temp_high': 20, 'temp_low': 12, 'rainfall': 45, 'conditions': 'Warm, longest days'},
                    'july': {'temp_high': 23, 'temp_low': 14, 'rainfall': 45, 'conditions': 'Warmest, pleasant'},
                    'august': {'temp_high': 22, 'temp_low': 14, 'rainfall': 49, 'conditions': 'Warm, variable'},
                    'september': {'temp_high': 19, 'temp_low': 12, 'rainfall': 49, 'conditions': 'Mild, autumn begins'},
                    'october': {'temp_high': 15, 'temp_low': 9, 'rainfall': 69, 'conditions': 'Cool, wet'},
                    'november': {'temp_high': 10, 'temp_low': 5, 'rainfall': 59, 'conditions': 'Cold, wet'},
                    'december': {'temp_high': 8, 'temp_low': 3, 'rainfall': 55, 'conditions': 'Cold, festive'}
                },
                'best_months': ['May', 'June', 'July', 'September'],
                'worst_months': ['November', 'December', 'January'],
                'peak_season': 'June-August',
                'off_season': 'November-February'
            }
        }
    
    def _load_packing_guides(self) -> Dict[str, Dict[str, List[str]]]:
        """Load packing recommendations by season"""
        return {
            'winter': {
                'clothing': [
                    'Heavy coat or winter jacket',
                    'Sweaters and warm layers',
                    'Long pants or jeans',
                    'Warm socks',
                    'Boots or waterproof shoes',
                    'Scarf, hat, gloves'
                ],
                'accessories': [
                    'Umbrella',
                    'Moisturizer for dry skin',
                    'Lip balm',
                    'Hand warmers'
                ]
            },
            'spring': {
                'clothing': [
                    'Light jacket or cardigan',
                    'Mix of short and long sleeves',
                    'Light pants and maybe shorts',
                    'Comfortable walking shoes',
                    'Light rain jacket'
                ],
                'accessories': [
                    'Sunglasses',
                    'Small umbrella',
                    'Sunscreen'
                ]
            },
            'summer': {
                'clothing': [
                    'Light, breathable clothing',
                    'T-shirts and tank tops',
                    'Shorts and light pants',
                    'Sundresses',
                    'Comfortable sandals',
                    'Sun hat or cap'
                ],
                'accessories': [
                    'Sunglasses',
                    'Sunscreen (high SPF)',
                    'Reusable water bottle',
                    'Light scarf for air-conditioned places'
                ]
            },
            'fall': {
                'clothing': [
                    'Medium-weight jacket',
                    'Layers (cardigans, sweaters)',
                    'Long pants and jeans',
                    'Closed-toe shoes',
                    'Light scarf'
                ],
                'accessories': [
                    'Umbrella',
                    'Sunglasses',
                    'Daypack for layers'
                ]
            }
        }
    
    def get_monthly_weather(
        self,
        destination: str,
        month: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get weather data for a specific month
        
        Args:
            destination: Destination name
            month: Month name
            
        Returns:
            Weather data or None
        """
        climate = self.climate_data.get(destination.lower())
        if climate and 'monthly_data' in climate:
            return climate['monthly_data'].get(month.lower())
        return None
    
    def get_best_time_to_visit(self, destination: str) -> Optional[List[str]]:
        """
        Get best months to visit
        
        Args:
            destination: Destination name
            
        Returns:
            List of best months
        """
        climate = self.climate_data.get(destination.lower())
        if climate:
            return climate.get('best_months')
        return None
    
    def get_season_for_month(self, month: str, hemisphere: str = 'north') -> str:
        """
        Determine season for a given month
        
        Args:
            month: Month name
            hemisphere: 'north' or 'south'
            
        Returns:
            Season name
        """
        month_lower = month.lower()
        
        if hemisphere == 'north':
            if month_lower in ['december', 'january', 'february']:
                return 'winter'
            elif month_lower in ['march', 'april', 'may']:
                return 'spring'
            elif month_lower in ['june', 'july', 'august']:
                return 'summer'
            else:
                return 'fall'
        else:  # southern hemisphere
            if month_lower in ['december', 'january', 'february']:
                return 'summer'
            elif month_lower in ['march', 'april', 'may']:
                return 'fall'
            elif month_lower in ['june', 'july', 'august']:
                return 'winter'
            else:
                return 'spring'
    
    def get_packing_list(
        self,
        destination: str,
        month: str
    ) -> Optional[Dict[str, List[str]]]:
        """
        Get packing recommendations for destination and time
        
        Args:
            destination: Destination name
            month: Month of travel
            
        Returns:
            Packing list dict
        """
        season = self.get_season_for_month(month)
        return self.packing_guides.get(season)
    
    def is_peak_season(self, destination: str, month: str) -> bool:
        """
        Check if month is peak season
        
        Args:
            destination: Destination name
            month: Month name
            
        Returns:
            True if peak season
        """
        climate = self.climate_data.get(destination.lower())
        if climate and 'best_months' in climate:
            return month.capitalize() in climate['best_months']
        return False
    
    def compare_months(
        self,
        destination: str,
        month1: str,
        month2: str
    ) -> str:
        """
        Compare two months for travel
        
        Args:
            destination: Destination name
            month1: First month
            month2: Second month
            
        Returns:
            Comparison summary
        """
        weather1 = self.get_monthly_weather(destination, month1)
        weather2 = self.get_monthly_weather(destination, month2)
        
        if not weather1 or not weather2:
            return "Unable to compare - insufficient data"
        
        comparison = f"{month1.capitalize()} vs {month2.capitalize()}:\n"
        comparison += f"Temperature: {weather1['temp_high']}°C vs {weather2['temp_high']}°C\n"
        comparison += f"Rainfall: {weather1['rainfall']}mm vs {weather2['rainfall']}mm\n"
        comparison += f"{month1.capitalize()}: {weather1['conditions']}\n"
        comparison += f"{month2.capitalize()}: {weather2['conditions']}"
        
        return comparison

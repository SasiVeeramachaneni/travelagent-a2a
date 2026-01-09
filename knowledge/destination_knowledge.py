"""
Destination Knowledge
Contains detailed information about travel destinations worldwide
"""
from typing import Dict, List, Optional, Any


class DestinationKnowledge:
    """
    Knowledge base for destination information
    
    This module provides:
    - Basic destination facts (country, region, language)
    - Best times to visit
    - Average budgets by tier
    - Top attractions and landmarks
    - Local cuisine specialties
    - Transportation options
    """
    
    def __init__(self):
        """Initialize destination knowledge base"""
        self.destinations = self._load_destinations()
    
    def _load_destinations(self) -> Dict[str, Any]:
        """
        Load destination database
        
        Structure:
        {
            'destination_name': {
                'country': str,
                'region': str,
                'language': [str],
                'currency': str,
                'best_months': [str],
                'avg_daily_budget': {'budget': int, 'moderate': int, 'luxury': int},
                'transportation': [str],
                'top_attractions': [str],
                'local_cuisine': [str],
                'population': int,
                'timezone': str
            }
        }
        """
        return {
            'paris': {
                'country': 'France',
                'region': 'Western Europe',
                'language': ['French', 'English (tourist areas)'],
                'currency': 'EUR (€)',
                'best_months': ['April', 'May', 'September', 'October'],
                'best_months_reason': 'Pleasant weather, fewer crowds than summer',
                'avg_daily_budget': {
                    'budget': 80,
                    'moderate': 150,
                    'luxury': 350
                },
                'transportation': ['Metro', 'Bus', 'Vélib (bike share)', 'Walking'],
                'top_attractions': [
                    'Eiffel Tower',
                    'Louvre Museum',
                    'Notre-Dame Cathedral',
                    'Arc de Triomphe',
                    'Sacré-Cœur Basilica',
                    'Versailles Palace',
                    'Musée d\'Orsay',
                    'Champs-Élysées'
                ],
                'local_cuisine': [
                    'Croissants & Pastries',
                    'Escargot (snails)',
                    'Coq au Vin',
                    'Crêpes',
                    'French Onion Soup',
                    'Macarons'
                ],
                'population': 2_161_000,
                'timezone': 'CET (UTC+1)',
                'climate': 'Temperate oceanic'
            },
            'tokyo': {
                'country': 'Japan',
                'region': 'East Asia',
                'language': ['Japanese', 'English (limited)'],
                'currency': 'JPY (¥)',
                'best_months': ['March', 'April', 'October', 'November'],
                'best_months_reason': 'Cherry blossoms (spring), fall foliage',
                'avg_daily_budget': {
                    'budget': 70,
                    'moderate': 130,
                    'luxury': 300
                },
                'transportation': ['Metro', 'JR Train', 'Bus', 'Taxi'],
                'top_attractions': [
                    'Senso-ji Temple',
                    'Tokyo Tower',
                    'Meiji Shrine',
                    'Shibuya Crossing',
                    'Tokyo Skytree',
                    'Imperial Palace',
                    'Tsukiji Fish Market',
                    'Akihabara'
                ],
                'local_cuisine': [
                    'Sushi',
                    'Ramen',
                    'Tempura',
                    'Wagyu Beef',
                    'Tonkatsu',
                    'Yakitori'
                ],
                'population': 13_960_000,
                'timezone': 'JST (UTC+9)',
                'climate': 'Humid subtropical'
            },
            'new york': {
                'country': 'United States',
                'region': 'North America - East Coast',
                'language': ['English', 'Spanish (common)'],
                'currency': 'USD ($)',
                'best_months': ['April', 'May', 'September', 'October', 'November'],
                'best_months_reason': 'Comfortable weather, fall colors, holiday season',
                'avg_daily_budget': {
                    'budget': 100,
                    'moderate': 200,
                    'luxury': 450
                },
                'transportation': ['Subway', 'Bus', 'Taxi/Uber', 'Walking'],
                'top_attractions': [
                    'Statue of Liberty',
                    'Central Park',
                    'Times Square',
                    'Empire State Building',
                    'Brooklyn Bridge',
                    'Metropolitan Museum of Art',
                    'One World Observatory',
                    'Broadway Shows'
                ],
                'local_cuisine': [
                    'New York Pizza',
                    'Bagels',
                    'Hot Dogs',
                    'Cheesecake',
                    'Pastrami Sandwich',
                    'Pretzels'
                ],
                'population': 8_336_000,
                'timezone': 'EST (UTC-5)',
                'climate': 'Humid subtropical'
            },
            'london': {
                'country': 'United Kingdom',
                'region': 'Western Europe',
                'language': ['English'],
                'currency': 'GBP (£)',
                'best_months': ['May', 'June', 'September', 'October'],
                'best_months_reason': 'Mild weather, parks in bloom, fewer tourists',
                'avg_daily_budget': {
                    'budget': 90,
                    'moderate': 180,
                    'luxury': 400
                },
                'transportation': ['Underground (Tube)', 'Bus', 'Black Cabs', 'Walking'],
                'top_attractions': [
                    'Big Ben & Parliament',
                    'Tower of London',
                    'British Museum',
                    'Buckingham Palace',
                    'London Eye',
                    'Tower Bridge',
                    'Westminster Abbey',
                    'Hyde Park'
                ],
                'local_cuisine': [
                    'Fish and Chips',
                    'Full English Breakfast',
                    'Afternoon Tea',
                    'Shepherd\'s Pie',
                    'Bangers and Mash',
                    'Sunday Roast'
                ],
                'population': 9_002_000,
                'timezone': 'GMT (UTC+0)',
                'climate': 'Temperate oceanic'
            }
        }
    
    def get_destination(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a destination
        
        Args:
            name: Destination name (case-insensitive)
            
        Returns:
            Dict with destination details or None if not found
        """
        return self.destinations.get(name.lower())
    
    def get_all_destinations(self) -> List[str]:
        """Get list of all available destinations"""
        return [dest.title() for dest in self.destinations.keys()]
    
    def search_by_region(self, region: str) -> List[str]:
        """
        Find destinations by region
        
        Args:
            region: Region name (e.g., 'Europe', 'Asia')
            
        Returns:
            List of matching destination names
        """
        matches = []
        for name, info in self.destinations.items():
            if region.lower() in info['region'].lower():
                matches.append(name.title())
        return matches
    
    def search_by_budget(self, max_daily_budget: float, tier: str = 'moderate') -> List[str]:
        """
        Find destinations within budget
        
        Args:
            max_daily_budget: Maximum daily budget
            tier: Budget tier ('budget', 'moderate', 'luxury')
            
        Returns:
            List of affordable destinations
        """
        matches = []
        for name, info in self.destinations.items():
            if info['avg_daily_budget'][tier] <= max_daily_budget:
                matches.append(name.title())
        return matches
    
    def get_best_time_to_visit(self, destination: str) -> Optional[Dict[str, Any]]:
        """
        Get best time to visit information
        
        Args:
            destination: Destination name
            
        Returns:
            Dict with best months and reasoning
        """
        dest = self.get_destination(destination)
        if dest:
            return {
                'months': dest['best_months'],
                'reason': dest.get('best_months_reason', 'Optimal weather and conditions')
            }
        return None
    
    def get_attractions(self, destination: str) -> Optional[List[str]]:
        """
        Get top attractions for a destination
        
        Args:
            destination: Destination name
            
        Returns:
            List of attraction names
        """
        dest = self.get_destination(destination)
        return dest['top_attractions'] if dest else None
    
    def get_local_cuisine(self, destination: str) -> Optional[List[str]]:
        """
        Get local cuisine specialties
        
        Args:
            destination: Destination name
            
        Returns:
            List of local dishes
        """
        dest = self.get_destination(destination)
        return dest['local_cuisine'] if dest else None

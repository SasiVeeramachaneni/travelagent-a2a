"""
Flight Knowledge
Contains information about flight routes, airlines, and booking tips
"""
from typing import Dict, List, Optional, Any


class FlightKnowledge:
    """
    Knowledge base for flight information
    
    This module provides:
    - Flight route information
    - Average flight durations
    - Major airlines by route
    - Booking tips and best practices
    - Seasonal pricing patterns
    - Airport information
    """
    
    def __init__(self):
        """Initialize flight knowledge base"""
        self.routes = self._load_routes()
        self.airlines = self._load_airlines()
        self.booking_tips = self._load_booking_tips()
    
    def _load_routes(self) -> Dict[str, Any]:
        """
        Load flight route information
        
        Structure:
        {
            'origin-destination': {
                'avg_duration_hours': float,
                'direct_available': bool,
                'common_layovers': [str],
                'major_airlines': [str],
                'avg_price_range': {'budget': int, 'moderate': int, 'luxury': int}
            }
        }
        """
        return {
            'india-paris': {
                'avg_duration_hours': 9.5,
                'direct_available': True,
                'common_layovers': ['Dubai', 'Doha', 'Frankfurt', 'Amsterdam'],
                'major_airlines': ['Air France', 'Air India', 'Emirates', 'Qatar Airways'],
                'avg_price_range': {
                    'budget': 650,
                    'moderate': 850,
                    'luxury': 1500
                }
            },
            'usa-paris': {
                'avg_duration_hours': 8.0,
                'direct_available': True,
                'common_layovers': ['London', 'Dublin', 'Reykjavik'],
                'major_airlines': ['Air France', 'Delta', 'United', 'American Airlines'],
                'avg_price_range': {
                    'budget': 500,
                    'moderate': 750,
                    'luxury': 2000
                }
            },
            'india-tokyo': {
                'avg_duration_hours': 7.5,
                'direct_available': True,
                'common_layovers': ['Singapore', 'Bangkok', 'Hong Kong'],
                'major_airlines': ['ANA', 'JAL', 'Air India', 'Singapore Airlines'],
                'avg_price_range': {
                    'budget': 550,
                    'moderate': 750,
                    'luxury': 1400
                }
            },
            'usa-tokyo': {
                'avg_duration_hours': 13.0,
                'direct_available': True,
                'common_layovers': ['Seoul', 'Taipei', 'Vancouver'],
                'major_airlines': ['ANA', 'JAL', 'United', 'American Airlines'],
                'avg_price_range': {
                    'budget': 700,
                    'moderate': 1000,
                    'luxury': 3000
                }
            }
        }
    
    def _load_airlines(self) -> Dict[str, Any]:
        """
        Load airline information
        
        Returns:
            Dict with airline details (baggage, amenities, ratings)
        """
        return {
            'Air France': {
                'type': 'Full Service',
                'checked_baggage': 1,
                'carry_on': 1,
                'rating': 4.2,
                'known_for': 'French cuisine, good service'
            },
            'Emirates': {
                'type': 'Full Service',
                'checked_baggage': 2,
                'carry_on': 1,
                'rating': 4.6,
                'known_for': 'Luxury, entertainment, excellent food'
            },
            'Air India': {
                'type': 'Full Service',
                'checked_baggage': 1,
                'carry_on': 1,
                'rating': 3.8,
                'known_for': 'Affordable, Indian cuisine'
            }
        }
    
    def _load_booking_tips(self) -> Dict[str, Any]:
        """Load flight booking tips and best practices"""
        return {
            'general': [
                'Book 2-3 months in advance for international flights',
                'Tuesday and Wednesday typically have lower prices',
                'Use incognito mode when searching to avoid price tracking',
                'Set up price alerts on comparison sites',
                'Consider nearby airports for better deals',
                'Be flexible with dates if possible'
            ],
            'timing': {
                'domestic': '1-2 months in advance',
                'international': '2-3 months in advance',
                'peak_season': '3-4 months in advance',
                'cheapest_days': ['Tuesday', 'Wednesday'],
                'avoid_days': ['Friday', 'Sunday']
            },
            'tools': [
                'Google Flights - Best for price tracking',
                'Skyscanner - Best for comparing multiple sites',
                'Kayak - Best for flexible date searches',
                'Hopper - Best for price predictions',
                'Direct airline websites - Best for loyalty points'
            ],
            'money_saving': [
                'Book connecting flights instead of direct',
                'Fly during off-peak hours (early morning, late night)',
                'Consider budget airlines for short routes',
                'Use airline miles and credit card points',
                'Book one-way tickets if cheaper than round-trip'
            ]
        }
    
    def get_route_info(self, origin: str, destination: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a flight route
        
        Args:
            origin: Origin city/region
            destination: Destination city
            
        Returns:
            Route information or None
        """
        route_key = f"{origin.lower()}-{destination.lower()}"
        return self.routes.get(route_key)
    
    def estimate_flight_price(
        self,
        origin: str,
        destination: str,
        tier: str = 'moderate'
    ) -> Optional[int]:
        """
        Estimate flight price for a route
        
        Args:
            origin: Origin location
            destination: Destination
            tier: Price tier ('budget', 'moderate', 'luxury')
            
        Returns:
            Estimated price or None
        """
        route = self.get_route_info(origin, destination)
        if route:
            return route['avg_price_range'].get(tier)
        return None
    
    def get_booking_tips(self, category: Optional[str] = None) -> Any:
        """
        Get flight booking tips
        
        Args:
            category: Specific category ('general', 'timing', 'tools', 'money_saving')
                     or None for all tips
            
        Returns:
            Tips for the category or all tips
        """
        if category:
            return self.booking_tips.get(category)
        return self.booking_tips
    
    def get_airline_info(self, airline: str) -> Optional[Dict[str, Any]]:
        """
        Get information about an airline
        
        Args:
            airline: Airline name
            
        Returns:
            Airline details or None
        """
        return self.airlines.get(airline)
    
    def recommend_airlines(self, origin: str, destination: str) -> List[str]:
        """
        Recommend airlines for a route
        
        Args:
            origin: Origin location
            destination: Destination
            
        Returns:
            List of recommended airlines
        """
        route = self.get_route_info(origin, destination)
        if route:
            return route['major_airlines']
        return []

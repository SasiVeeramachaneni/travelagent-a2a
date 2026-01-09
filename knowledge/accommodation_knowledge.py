"""
Accommodation Knowledge
Contains information about hotels, hostels, vacation rentals, and booking strategies
"""
from typing import Dict, List, Optional, Any


class AccommodationKnowledge:
    """
    Knowledge base for accommodation information
    
    This module provides:
    - Average prices by destination and type
    - Popular accommodation platforms
    - Neighborhood recommendations
    - Booking tips and strategies
    - Amenity information
    """
    
    def __init__(self):
        """Initialize accommodation knowledge base"""
        self.pricing = self._load_pricing()
        self.neighborhoods = self._load_neighborhoods()
        self.booking_tips = self._load_booking_tips()
        self.platforms = self._load_platforms()
    
    def _load_pricing(self) -> Dict[str, Any]:
        """
        Load accommodation pricing by destination
        
        Structure:
        {
            'destination': {
                'hostel': price_per_night,
                'budget_hotel': price_per_night,
                'hotel': price_per_night,
                'vacation_rental': price_per_night,
                'luxury': price_per_night
            }
        }
        """
        return {
            'paris': {
                'hostel': 35,
                'budget_hotel': 75,
                'hotel': 150,
                'vacation_rental': 120,
                'luxury': 350,
                'currency': 'USD'
            },
            'tokyo': {
                'hostel': 30,
                'budget_hotel': 60,
                'hotel': 120,
                'vacation_rental': 100,
                'luxury': 300,
                'currency': 'USD'
            },
            'new york': {
                'hostel': 50,
                'budget_hotel': 120,
                'hotel': 200,
                'vacation_rental': 160,
                'luxury': 450,
                'currency': 'USD'
            },
            'london': {
                'hostel': 40,
                'budget_hotel': 90,
                'hotel': 180,
                'vacation_rental': 140,
                'luxury': 400,
                'currency': 'USD'
            }
        }
    
    def _load_neighborhoods(self) -> Dict[str, Any]:
        """
        Load neighborhood recommendations by destination
        """
        return {
            'paris': {
                'best_for_tourists': [
                    'Le Marais - Central, trendy, walkable',
                    'Latin Quarter - Historic, student vibe',
                    'Saint-Germain-des-Prés - Upscale, artistic'
                ],
                'budget_friendly': [
                    'Montmartre - Bohemian, cheaper than center',
                    'Belleville - Diverse, authentic',
                    ' 13th Arrondissement - Asian quarter, affordable'
                ],
                'luxury': [
                    'Champs-Élysées - Iconic, expensive',
                    '7th Arrondissement - Eiffel Tower area',
                    '8th Arrondissement - High-end shopping'
                ]
            },
            'tokyo': {
                'best_for_tourists': [
                    'Shinjuku - Transport hub, vibrant nightlife',
                    'Shibuya - Modern, shopping, entertainment',
                    'Asakusa - Traditional, near temples'
                ],
                'budget_friendly': [
                    'Ikebukuro - Good value, less touristy',
                    'Ueno - Parks, museums, affordable',
                    'Akihabara - Tech district, reasonable prices'
                ],
                'luxury': [
                    'Ginza - Upscale shopping, dining',
                    'Roppongi - International, high-end',
                    'Marunouchi - Business district, premium'
                ]
            }
        }
    
    def _load_booking_tips(self) -> Dict[str, Any]:
        """Load accommodation booking tips"""
        return {
            'general': [
                'Book 1-2 months in advance for best prices',
                'Check cancellation policies before booking',
                'Read recent reviews (within 6 months)',
                'Verify location on a map before booking',
                'Compare prices across multiple platforms',
                'Check if breakfast is included'
            ],
            'timing': {
                'advance_booking': '1-2 months for best prices',
                'last_minute': 'Can find deals but risky in peak season',
                'cheapest_days': 'Sunday-Thursday check-ins',
                'expensive_days': 'Friday-Saturday check-ins'
            },
            'money_saving': [
                'Stay slightly outside tourist areas',
                'Book longer stays for discounts',
                'Consider vacation rentals for groups',
                'Look for accommodations with kitchens',
                'Join loyalty programs for points',
                'Book directly with hotel for perks'
            ],
            'red_flags': [
                'No recent reviews or photos',
                'Prices much lower than comparable options',
                'Vague location descriptions',
                'No cancellation policy',
                'Poor response time to inquiries',
                'Requests for wire transfers'
            ]
        }
    
    def _load_platforms(self) -> Dict[str, Any]:
        """Load booking platform information"""
        return {
            'Booking.com': {
                'type': 'Hotels & Apartments',
                'pros': ['Free cancellation options', 'Loyalty program', 'Wide selection'],
                'cons': ['Sometimes higher prices'],
                'best_for': 'Hotels with flexible cancellation'
            },
            'Airbnb': {
                'type': 'Vacation Rentals',
                'pros': ['Unique properties', 'Kitchen facilities', 'Local experience'],
                'cons': ['Cleaning fees', 'Less standardized', 'Service fees'],
                'best_for': 'Longer stays, groups, local experience'
            },
            'Hostelworld': {
                'type': 'Hostels',
                'pros': ['Best hostel selection', 'Social atmosphere', 'Budget-friendly'],
                'cons': ['Limited to hostels'],
                'best_for': 'Solo travelers, budget backpackers'
            },
            'Hotels.com': {
                'type': 'Hotels',
                'pros': ['Rewards program (10 nights = 1 free)', 'Price match'],
                'cons': ['Limited vacation rentals'],
                'best_for': 'Frequent hotel stays'
            },
            'Vrbo': {
                'type': 'Vacation Rentals',
                'pros': ['No service fees', 'Entire properties', 'Family-friendly'],
                'cons': ['Smaller selection than Airbnb'],
                'best_for': 'Families, entire home rentals'
            }
        }
    
    def get_pricing(self, destination: str, accommodation_type: str) -> Optional[float]:
        """
        Get average nightly price for accommodation
        
        Args:
            destination: Destination name
            accommodation_type: Type ('hostel', 'budget_hotel', 'hotel', etc.)
            
        Returns:
            Average price per night or None
        """
        dest_pricing = self.pricing.get(destination.lower())
        if dest_pricing:
            return dest_pricing.get(accommodation_type)
        return None
    
    def get_neighborhood_recommendations(
        self,
        destination: str,
        category: Optional[str] = None
    ) -> Any:
        """
        Get neighborhood recommendations
        
        Args:
            destination: Destination name
            category: 'best_for_tourists', 'budget_friendly', or 'luxury'
            
        Returns:
            Neighborhood recommendations
        """
        dest_neighborhoods = self.neighborhoods.get(destination.lower())
        if dest_neighborhoods:
            if category:
                return dest_neighborhoods.get(category)
            return dest_neighborhoods
        return None
    
    def get_booking_tips(self, category: Optional[str] = None) -> Any:
        """
        Get booking tips
        
        Args:
            category: 'general', 'timing', 'money_saving', or 'red_flags'
            
        Returns:
            Tips for category or all tips
        """
        if category:
            return self.booking_tips.get(category)
        return self.booking_tips
    
    def get_platform_info(self, platform: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a booking platform
        
        Args:
            platform: Platform name
            
        Returns:
            Platform details or None
        """
        return self.platforms.get(platform)
    
    def recommend_platforms(self, accommodation_type: str) -> List[str]:
        """
        Recommend booking platforms based on accommodation type
        
        Args:
            accommodation_type: Type of accommodation
            
        Returns:
            List of recommended platforms
        """
        recommendations = []
        
        if accommodation_type == 'hostel':
            recommendations = ['Hostelworld', 'Booking.com']
        elif accommodation_type in ['hotel', 'budget_hotel', 'luxury']:
            recommendations = ['Booking.com', 'Hotels.com']
        elif accommodation_type == 'vacation_rental':
            recommendations = ['Airbnb', 'Vrbo']
        
        return recommendations
    
    def calculate_total_cost(
        self,
        destination: str,
        accommodation_type: str,
        nights: int
    ) -> Optional[float]:
        """
        Calculate total accommodation cost
        
        Args:
            destination: Destination name
            accommodation_type: Type of accommodation
            nights: Number of nights
            
        Returns:
            Total cost or None
        """
        price_per_night = self.get_pricing(destination, accommodation_type)
        if price_per_night:
            return price_per_night * nights
        return None

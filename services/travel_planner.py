"""
Travel Planner Service
Handles destination research, recommendations, and travel planning logic
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

# Import knowledge base modules
try:
    from knowledge import (
        DestinationKnowledge,
        FlightKnowledge,
        AccommodationKnowledge,
        ActivityKnowledge,
        VisaKnowledge,
        WeatherKnowledge,
        CulturalKnowledge,
        SafetyKnowledge
    )
    KNOWLEDGE_AVAILABLE = True
except ImportError:
    KNOWLEDGE_AVAILABLE = False


class TravelPlanner:
    """
    Service for travel planning, destination research, and recommendations
    """
    
    def __init__(self):
        """Initialize travel planner with knowledge base"""
        self.destination_data = self._load_destination_data()
        
        # Initialize knowledge base modules if available
        if KNOWLEDGE_AVAILABLE:
            self.destinations = DestinationKnowledge()
            self.flights = FlightKnowledge()
            self.accommodations = AccommodationKnowledge()
            self.activities = ActivityKnowledge()
            self.visas = VisaKnowledge()
            self.weather = WeatherKnowledge()
            self.culture = CulturalKnowledge()
            self.safety = SafetyKnowledge()
    
    def _load_destination_data(self) -> Dict[str, Any]:
        """
        Load destination data
        In a real implementation, this would connect to external APIs
        
        Returns:
            Dict: Destination information database
        """
        return {
            'paris': {
                'country': 'France',
                'best_months': ['April', 'May', 'September', 'October'],
                'avg_daily_budget': {'budget': 80, 'moderate': 150, 'luxury': 350},
                'transportation': ['metro', 'bus', 'bike', 'walking'],
                'top_attractions': [
                    'Eiffel Tower',
                    'Louvre Museum',
                    'Notre-Dame Cathedral',
                    'Arc de Triomphe',
                    'Sacré-Cœur'
                ],
                'local_cuisine': ['Croissants', 'Escargot', 'Coq au Vin', 'Crêpes'],
                'safety_rating': 8.5,
                'visa_info': 'Schengen visa required for most non-EU citizens'
            },
            'tokyo': {
                'country': 'Japan',
                'best_months': ['March', 'April', 'October', 'November'],
                'avg_daily_budget': {'budget': 70, 'moderate': 130, 'luxury': 300},
                'transportation': ['metro', 'train', 'bus'],
                'top_attractions': [
                    'Senso-ji Temple',
                    'Tokyo Tower',
                    'Meiji Shrine',
                    'Shibuya Crossing',
                    'Tokyo Skytree'
                ],
                'local_cuisine': ['Sushi', 'Ramen', 'Tempura', 'Wagyu'],
                'safety_rating': 9.5,
                'visa_info': 'Visa-free for many countries (up to 90 days)'
            },
            'new york': {
                'country': 'USA',
                'best_months': ['April', 'May', 'September', 'October', 'November'],
                'avg_daily_budget': {'budget': 100, 'moderate': 200, 'luxury': 450},
                'transportation': ['subway', 'bus', 'taxi', 'walking'],
                'top_attractions': [
                    'Statue of Liberty',
                    'Central Park',
                    'Times Square',
                    'Empire State Building',
                    'Brooklyn Bridge'
                ],
                'local_cuisine': ['Pizza', 'Bagels', 'Hot Dogs', 'Cheesecake'],
                'safety_rating': 7.5,
                'visa_info': 'ESTA or visa required for most international visitors'
            }
        }
    
    def generate_recommendations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized travel recommendations
        
        Args:
            context: User context with preferences
            
        Returns:
            Dict: Travel recommendations
        """
        destination = context.get('destination', '').lower()
        budget_level = context.get('budget_level', 'moderate')
        interests = context.get('interests', [])
        
        recommendations = {
            'destinations': [],
            'activities': [],
            'accommodations': [],
            'dining': [],
            'transport': []
        }
        
        # Get destination-specific recommendations
        if destination in self.destination_data:
            dest_info = self.destination_data[destination]
            
            # Activity recommendations based on interests
            if 'culture' in interests:
                recommendations['activities'].extend([
                    f"Visit {dest_info['top_attractions'][0]}",
                    f"Explore {dest_info['top_attractions'][1]}"
                ])
            
            if 'food' in interests:
                recommendations['dining'].extend([
                    f"Try local {dest_info['local_cuisine'][0]}",
                    f"Experience {dest_info['local_cuisine'][1]}"
                ])
            
            # Accommodation recommendations
            recommendations['accommodations'] = self._get_accommodation_recommendations(
                destination,
                budget_level
            )
            
            # Transport recommendations
            recommendations['transport'] = dest_info['transportation']
        
        return recommendations
    
    def get_destination_recommendations(
        self,
        destination: str,
        interests: List[str],
        budget: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Get detailed recommendations for a specific destination
        
        Args:
            destination: Destination name
            interests: List of user interests
            budget: Optional budget constraint
            
        Returns:
            Dict: Detailed recommendations
        """
        destination = destination.lower()
        
        if destination not in self.destination_data:
            return {
                'message': f"I'd love to help you explore {destination}! Let me research the best options for you."
            }
        
        dest_info = self.destination_data[destination]
        
        return {
            'destination': destination.title(),
            'best_time_to_visit': dest_info['best_months'],
            'top_attractions': dest_info['top_attractions'][:5],
            'local_experiences': dest_info['local_cuisine'],
            'transportation_options': dest_info['transportation'],
            'safety_rating': dest_info['safety_rating']
        }
    
    def _get_accommodation_recommendations(
        self,
        destination: str,
        budget_level: str
    ) -> List[str]:
        """
        Get accommodation recommendations based on budget level
        
        Args:
            destination: Destination name
            budget_level: Budget level (budget, moderate, luxury)
            
        Returns:
            List[str]: Accommodation recommendations
        """
        accommodations = {
            'budget': [
                'Hostels in central locations',
                'Budget hotels near public transport',
                'Shared Airbnb accommodations'
            ],
            'moderate': [
                '3-star hotels in good neighborhoods',
                'Boutique hotels',
                'Private Airbnb apartments',
                'Bed & Breakfast establishments'
            ],
            'luxury': [
                '5-star hotels with full amenities',
                'Luxury boutique hotels',
                'Premium vacation rentals',
                'Resort properties'
            ]
        }
        
        return accommodations.get(budget_level, accommodations['moderate'])
    
    def get_flight_recommendations(
        self,
        origin: str,
        destination: str,
        departure_date: Optional[datetime] = None,
        return_date: Optional[datetime] = None,
        budget_level: str = 'moderate'
    ) -> Dict[str, Any]:
        """
        Get flight recommendations
        
        Args:
            origin: Origin city/airport
            destination: Destination city/airport
            departure_date: Departure date
            return_date: Return date
            budget_level: Budget level
            
        Returns:
            Dict: Flight recommendations
        """
        # In a real implementation, this would call flight APIs
        return {
            'recommendation': (
                f"For flights from {origin} to {destination}, I recommend:\n"
                "• Booking 2-3 months in advance for best prices\n"
                "• Comparing prices on Skyscanner, Google Flights, and Kayak\n"
                "• Considering connecting flights for budget options\n"
                "• Checking both departure and nearby airports"
            ),
            'tips': [
                'Be flexible with dates if possible',
                'Set up price alerts',
                'Clear browser cookies before booking',
                'Book on Tuesdays or Wednesdays for better deals'
            ]
        }
    
    def get_travel_support_info(self, destination: str) -> Dict[str, Any]:
        """
        Get travel support information for a destination
        
        Args:
            destination: Destination name
            
        Returns:
            Dict: Travel support information
        """
        destination = destination.lower()
        
        if destination not in self.destination_data:
            return {
                'message': 'Please provide more details about your destination.'
            }
        
        dest_info = self.destination_data[destination]
        
        return {
            'visa_requirements': dest_info.get('visa_info', 'Please check official sources'),
            'safety_tips': [
                f"Safety rating: {dest_info['safety_rating']}/10",
                'Keep copies of important documents',
                'Register with your embassy',
                'Purchase comprehensive travel insurance',
                'Keep emergency contacts handy'
            ],
            'emergency_contacts': (
                'Local Emergency: 112 (Europe) / 911 (US)\n'
                'Tourist Police: Check local numbers\n'
                'Embassy: Contact your country\'s embassy'
            ),
            'health_tips': [
                'Check vaccination requirements',
                'Bring necessary medications',
                'Research local healthcare facilities',
                'Consider travel health insurance'
            ]
        }
    
    def get_knowledge_based_info(
        self,
        destination: str,
        info_type: str
    ) -> Optional[Any]:
        """
        Get information from knowledge base modules
        
        Args:
            destination: Destination name
            info_type: Type of info ('weather', 'visa', 'culture', 'safety', 'activities')
            
        Returns:
            Information from knowledge base or None
        """
        if not KNOWLEDGE_AVAILABLE:
            return None
        
        destination = destination.lower()
        
        if info_type == 'weather':
            return self.weather.get_best_time_to_visit(destination)
        elif info_type == 'visa':
            return self.visas.get_general_tips()
        elif info_type == 'culture':
            return self.culture.get_cultural_info(destination)
        elif info_type == 'safety':
            return self.safety.get_safety_info(destination)
        elif info_type == 'activities':
            return self.activities.get_activities(destination)
        elif info_type == 'accommodation':
            return self.accommodations.get_pricing(destination)
        
        return None
    
    def calculate_optimal_duration(
        self,
        destination: str,
        interests: List[str]
    ) -> int:
        """
        Calculate optimal trip duration based on destination and interests
        
        Args:
            destination: Destination name
            interests: User interests
            
        Returns:
            int: Recommended number of days
        """
        base_duration = 3  # Base minimum
        
        # Add days based on interests
        interest_days = {
            'culture': 2,
            'adventure': 3,
            'food': 1,
            'relaxation': 2,
            'nightlife': 1,
            'shopping': 1
        }
        
        additional_days = sum(interest_days.get(interest, 0) for interest in interests)
        
        return min(base_duration + additional_days, 14)  # Cap at 2 weeks
    
    def get_seasonal_recommendations(
        self,
        month: str,
        preferences: Dict[str, Any]
    ) -> List[str]:
        """
        Get destination recommendations based on season
        
        Args:
            month: Month of travel
            preferences: User preferences
            
        Returns:
            List[str]: Recommended destinations
        """
        recommendations = []
        
        for dest_name, dest_info in self.destination_data.items():
            if month in dest_info['best_months']:
                recommendations.append(dest_name.title())
        
        return recommendations

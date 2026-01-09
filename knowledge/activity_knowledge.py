"""
Activity Knowledge
Contains information about activities, tours, attractions, and experiences
"""
from typing import Dict, List, Optional, Any


class ActivityKnowledge:
    """
    Knowledge base for activities and attractions
    
    This module provides:
    - Popular activities by destination
    - Entry fees and pricing
    - Operating hours
    - Booking requirements
    - Activity categories (culture, adventure, food, etc.)
    """
    
    def __init__(self):
        """Initialize activity knowledge base"""
        self.activities = self._load_activities()
        self.categories = self._load_categories()
    
    def _load_activities(self) -> Dict[str, Any]:
        """
        Load activity database
        
        Structure:
        {
            'destination': {
                'activity_name': {
                    'category': str,
                    'duration': hours,
                    'cost': float,
                    'booking_required': bool,
                    'best_time': str,
                    'description': str
                }
            }
        }
        """
        return {
            'paris': {
                'Eiffel Tower Visit': {
                    'category': 'landmark',
                    'duration': 2,
                    'cost': 26,
                    'booking_required': True,
                    'best_time': 'Early morning or evening',
                    'description': 'Iconic iron tower with observation decks'
                },
                'Louvre Museum': {
                    'category': 'culture',
                    'duration': 3,
                    'cost': 17,
                    'booking_required': True,
                    'best_time': 'Weekday mornings',
                    'description': 'World\'s largest art museum, home to Mona Lisa'
                },
                'Seine River Cruise': {
                    'category': 'sightseeing',
                    'duration': 1.5,
                    'cost': 15,
                    'booking_required': False,
                    'best_time': 'Evening for illuminated views',
                    'description': 'Boat tour along the Seine River'
                },
                'Versailles Palace Tour': {
                    'category': 'culture',
                    'duration': 4,
                    'cost': 27,
                    'booking_required': True,
                    'best_time': 'Weekday mornings',
                    'description': 'Royal palace with stunning gardens'
                },
                'Montmartre Walking Tour': {
                    'category': 'walking',
                    'duration': 3,
                    'cost': 0,
                    'booking_required': False,
                    'best_time': 'Morning or afternoon',
                    'description': 'Artistic neighborhood with Sacré-Cœur'
                },
                'French Cooking Class': {
                    'category': 'food',
                    'duration': 3,
                    'cost': 95,
                    'booking_required': True,
                    'best_time': 'Morning or afternoon',
                    'description': 'Learn to cook French cuisine'
                }
            },
            'tokyo': {
                'Senso-ji Temple': {
                    'category': 'culture',
                    'duration': 1.5,
                    'cost': 0,
                    'booking_required': False,
                    'best_time': 'Early morning',
                    'description': 'Ancient Buddhist temple in Asakusa'
                },
                'Tokyo Skytree': {
                    'category': 'landmark',
                    'duration': 2,
                    'cost': 18,
                    'booking_required': True,
                    'best_time': 'Sunset',
                    'description': 'Tallest structure in Japan with observation decks'
                },
                'Tsukiji Fish Market': {
                    'category': 'food',
                    'duration': 2,
                    'cost': 0,
                    'booking_required': False,
                    'best_time': 'Early morning (before 9 AM)',
                    'description': 'Famous fish market and sushi breakfast'
                },
                'Meiji Shrine Visit': {
                    'category': 'culture',
                    'duration': 1.5,
                    'cost': 0,
                    'booking_required': False,
                    'best_time': 'Morning',
                    'description': 'Shinto shrine in forested grounds'
                },
                'Robot Restaurant Show': {
                    'category': 'entertainment',
                    'duration': 2,
                    'cost': 60,
                    'booking_required': True,
                    'best_time': 'Evening',
                    'description': 'Futuristic robot and laser show'
                },
                'Sumo Wrestling Match': {
                    'category': 'sports',
                    'duration': 4,
                    'cost': 50,
                    'booking_required': True,
                    'best_time': 'During tournament season',
                    'description': 'Traditional Japanese wrestling'
                }
            },
            'new york': {
                'Statue of Liberty & Ellis Island': {
                    'category': 'landmark',
                    'duration': 4,
                    'cost': 24,
                    'booking_required': True,
                    'best_time': 'Morning (less crowded)',
                    'description': 'Iconic statue and immigration museum'
                },
                'Central Park': {
                    'category': 'nature',
                    'duration': 2,
                    'cost': 0,
                    'booking_required': False,
                    'best_time': 'Afternoon',
                    'description': 'Urban park with walking trails and attractions'
                },
                'Broadway Show': {
                    'category': 'entertainment',
                    'duration': 2.5,
                    'cost': 100,
                    'booking_required': True,
                    'best_time': 'Evening',
                    'description': 'World-famous theater performances'
                },
                'Metropolitan Museum': {
                    'category': 'culture',
                    'duration': 3,
                    'cost': 25,
                    'booking_required': False,
                    'best_time': 'Weekday mornings',
                    'description': 'One of the world\'s largest art museums'
                },
                'Food Tour': {
                    'category': 'food',
                    'duration': 3,
                    'cost': 75,
                    'booking_required': True,
                    'best_time': 'Lunch or dinner time',
                    'description': 'Taste iconic NYC foods across neighborhoods'
                }
            }
        }
    
    def _load_categories(self) -> Dict[str, str]:
        """Load activity category descriptions"""
        return {
            'landmark': 'Iconic structures and monuments',
            'culture': 'Museums, temples, historical sites',
            'sightseeing': 'Tours and scenic viewpoints',
            'food': 'Culinary experiences and food tours',
            'nature': 'Parks, gardens, outdoor spaces',
            'adventure': 'Active and adventure activities',
            'entertainment': 'Shows, performances, nightlife',
            'shopping': 'Markets, malls, boutiques',
            'sports': 'Sporting events and activities',
            'walking': 'Self-guided walking tours'
        }
    
    def get_activities(
        self,
        destination: str,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get activities for a destination
        
        Args:
            destination: Destination name
            category: Filter by category (optional)
            
        Returns:
            Dict of activities
        """
        dest_activities = self.activities.get(destination.lower(), {})
        
        if category:
            return {
                name: info for name, info in dest_activities.items()
                if info['category'] == category
            }
        
        return dest_activities
    
    def get_activity_details(
        self,
        destination: str,
        activity_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific activity
        
        Args:
            destination: Destination name
            activity_name: Activity name
            
        Returns:
            Activity details or None
        """
        dest_activities = self.activities.get(destination.lower(), {})
        return dest_activities.get(activity_name)
    
    def get_free_activities(self, destination: str) -> List[str]:
        """
        Get free activities for a destination
        
        Args:
            destination: Destination name
            
        Returns:
            List of free activity names
        """
        dest_activities = self.activities.get(destination.lower(), {})
        return [
            name for name, info in dest_activities.items()
            if info['cost'] == 0
        ]
    
    def calculate_activity_cost(
        self,
        destination: str,
        activity_names: List[str]
    ) -> float:
        """
        Calculate total cost for selected activities
        
        Args:
            destination: Destination name
            activity_names: List of activity names
            
        Returns:
            Total cost
        """
        total = 0.0
        dest_activities = self.activities.get(destination.lower(), {})
        
        for name in activity_names:
            if name in dest_activities:
                total += dest_activities[name]['cost']
        
        return total
    
    def get_activities_by_interest(
        self,
        destination: str,
        interests: List[str]
    ) -> List[str]:
        """
        Get activities matching user interests
        
        Args:
            destination: Destination name
            interests: List of interest categories
            
        Returns:
            List of matching activity names
        """
        dest_activities = self.activities.get(destination.lower(), {})
        matches = []
        
        for name, info in dest_activities.items():
            if info['category'] in interests:
                matches.append(name)
        
        return matches
    
    def get_booking_required_activities(self, destination: str) -> List[str]:
        """
        Get activities that require advance booking
        
        Args:
            destination: Destination name
            
        Returns:
            List of activity names
        """
        dest_activities = self.activities.get(destination.lower(), {})
        return [
            name for name, info in dest_activities.items()
            if info['booking_required']
        ]
    
    def estimate_daily_activity_cost(
        self,
        destination: str,
        budget_level: str = 'moderate'
    ) -> float:
        """
        Estimate average daily activity cost
        
        Args:
            destination: Destination name
            budget_level: 'budget', 'moderate', or 'luxury'
            
        Returns:
            Estimated daily cost
        """
        estimates = {
            'budget': 15,
            'moderate': 35,
            'luxury': 75
        }
        
        return estimates.get(budget_level, 35)

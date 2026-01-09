"""
Itinerary Manager Service
Creates and manages detailed day-by-day travel itineraries
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta


class ItineraryManager:
    """
    Service for creating and managing detailed travel itineraries
    """
    
    def __init__(self):
        """Initialize itinerary manager"""
        self.itinerary_templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Any]:
        """
        Load itinerary templates for different destinations
        
        Returns:
            Dict: Itinerary templates
        """
        return {
            'paris': {
                'day_plans': [
                    {
                        'title': 'Arrival & Iconic Landmarks',
                        'morning': [
                            {'time': '9:00 AM', 'activity': 'Check-in to hotel', 'duration': 30},
                            {'time': '10:00 AM', 'activity': 'Visit Eiffel Tower', 'duration': 120, 'cost': 26}
                        ],
                        'afternoon': [
                            {'time': '1:00 PM', 'activity': 'Lunch at local café', 'duration': 90, 'cost': 25},
                            {'time': '3:00 PM', 'activity': 'Seine River cruise', 'duration': 90, 'cost': 15}
                        ],
                        'evening': [
                            {'time': '6:00 PM', 'activity': 'Explore Champs-Élysées', 'duration': 120},
                            {'time': '8:00 PM', 'activity': 'Dinner in Latin Quarter', 'duration': 120, 'cost': 35}
                        ]
                    },
                    {
                        'title': 'Art & Culture',
                        'morning': [
                            {'time': '9:00 AM', 'activity': 'Louvre Museum visit', 'duration': 180, 'cost': 17}
                        ],
                        'afternoon': [
                            {'time': '1:00 PM', 'activity': 'Lunch near museum', 'duration': 90, 'cost': 20},
                            {'time': '3:00 PM', 'activity': 'Tuileries Garden walk', 'duration': 60},
                            {'time': '4:30 PM', 'activity': 'Musée d\'Orsay', 'duration': 120, 'cost': 14}
                        ],
                        'evening': [
                            {'time': '7:00 PM', 'activity': 'Montmartre & Sacré-Cœur', 'duration': 120},
                            {'time': '9:00 PM', 'activity': 'Dinner in Montmartre', 'duration': 120, 'cost': 30}
                        ]
                    }
                ]
            },
            'tokyo': {
                'day_plans': [
                    {
                        'title': 'Traditional Tokyo',
                        'morning': [
                            {'time': '8:00 AM', 'activity': 'Visit Senso-ji Temple', 'duration': 120},
                            {'time': '10:30 AM', 'activity': 'Explore Nakamise Street', 'duration': 60}
                        ],
                        'afternoon': [
                            {'time': '12:00 PM', 'activity': 'Sushi lunch', 'duration': 90, 'cost': 25},
                            {'time': '2:00 PM', 'activity': 'Meiji Shrine visit', 'duration': 90},
                            {'time': '4:00 PM', 'activity': 'Harajuku shopping', 'duration': 120}
                        ],
                        'evening': [
                            {'time': '7:00 PM', 'activity': 'Shibuya Crossing', 'duration': 60},
                            {'time': '8:00 PM', 'activity': 'Izakaya dinner', 'duration': 120, 'cost': 35}
                        ]
                    }
                ]
            }
        }
    
    def create_itinerary(
        self,
        destination: str,
        duration: int,
        interests: List[str],
        budget: Optional[float] = None,
        accommodation_pref: Optional[str] = None,
        transport_pref: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a detailed day-by-day itinerary
        
        Args:
            destination: Destination name
            duration: Number of days
            interests: List of interests
            budget: Total budget (optional)
            accommodation_pref: Accommodation preference (optional)
            transport_pref: Local transport preference (optional)
            
        Returns:
            Dict: Complete itinerary
        """
        destination_key = destination.lower()
        
        itinerary = {
            'title': f'{duration}-Day Trip to {destination.title()}',
            'destination': destination.title(),
            'duration': duration,
            'days': []
        }
        
        # Add Day 0 (Arrival)
        itinerary['days'].append(self._create_arrival_day(destination, accommodation_pref))
        
        # Add main days
        if destination_key in self.itinerary_templates:
            template_days = self.itinerary_templates[destination_key]['day_plans']
            
            # Use templates and repeat if necessary
            for day_num in range(1, duration):
                template_index = (day_num - 1) % len(template_days)
                day_plan = self._create_day_from_template(
                    day_num,
                    template_days[template_index],
                    interests,
                    transport_pref
                )
                itinerary['days'].append(day_plan)
        else:
            # Generate generic itinerary
            for day_num in range(1, duration):
                itinerary['days'].append(
                    self._create_generic_day(day_num, destination, interests)
                )
        
        # Add departure day
        itinerary['days'].append(self._create_departure_day(duration))
        
        return itinerary
    
    def _create_arrival_day(
        self,
        destination: str,
        accommodation_pref: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create arrival day plan
        
        Args:
            destination: Destination name
            accommodation_pref: Accommodation preference
            
        Returns:
            Dict: Arrival day plan
        """
        return {
            'day_number': 0,
            'title': 'Arrival Day',
            'description': f'Arrive in {destination.title()} and settle in',
            'activities': [
                {
                    'time': 'Upon Arrival',
                    'name': 'Airport to Hotel Transfer',
                    'details': 'Take airport shuttle, taxi, or public transport to accommodation',
                    'cost': 'Varies by transport method',
                    'duration': '30-60 minutes'
                },
                {
                    'time': 'Afternoon',
                    'name': 'Hotel Check-in',
                    'details': 'Check into your accommodation and freshen up',
                    'duration': '30 minutes'
                },
                {
                    'time': 'Evening',
                    'name': 'Light exploration & dinner',
                    'details': 'Take a relaxed walk around your neighborhood and find a local restaurant',
                    'cost': '$25-40',
                    'duration': '2-3 hours'
                }
            ],
            'daily_total': '$50-80',
            'notes': 'Rest and adjust to the new time zone'
        }
    
    def _create_departure_day(self, day_number: int) -> Dict[str, Any]:
        """
        Create departure day plan
        
        Args:
            day_number: Day number
            
        Returns:
            Dict: Departure day plan
        """
        return {
            'day_number': day_number,
            'title': 'Departure Day',
            'description': 'Check-out and head to airport',
            'activities': [
                {
                    'time': 'Morning',
                    'name': 'Hotel Check-out',
                    'details': 'Pack and check out of accommodation',
                    'duration': '30 minutes'
                },
                {
                    'time': 'Mid-Morning',
                    'name': 'Last-minute shopping or sightseeing',
                    'details': 'If time permits before flight',
                    'duration': '1-2 hours (optional)'
                },
                {
                    'time': 'Before Flight',
                    'name': 'Transfer to Airport',
                    'details': 'Leave with plenty of time for international flights (3 hours recommended)',
                    'cost': 'Varies by transport'
                }
            ],
            'notes': 'Arrive at airport 3 hours before international flights'
        }
    
    def _create_day_from_template(
        self,
        day_number: int,
        template: Dict[str, Any],
        interests: List[str],
        transport_pref: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create day plan from template
        
        Args:
            day_number: Day number
            template: Template dictionary
            interests: User interests
            transport_pref: Transport preference
            
        Returns:
            Dict: Day plan
        """
        activities = []
        daily_cost = 0
        
        # Morning activities
        for activity in template.get('morning', []):
            activities.append({
                'time': activity['time'],
                'name': activity['activity'],
                'details': f"Duration: ~{activity['duration']} minutes",
                'cost': f"${activity['cost']}" if 'cost' in activity else 'Free'
            })
            if 'cost' in activity:
                daily_cost += activity['cost']
        
        # Afternoon activities
        for activity in template.get('afternoon', []):
            activities.append({
                'time': activity['time'],
                'name': activity['activity'],
                'details': f"Duration: ~{activity['duration']} minutes",
                'cost': f"${activity['cost']}" if 'cost' in activity else 'Free'
            })
            if 'cost' in activity:
                daily_cost += activity['cost']
        
        # Evening activities
        for activity in template.get('evening', []):
            activities.append({
                'time': activity['time'],
                'name': activity['activity'],
                'details': f"Duration: ~{activity['duration']} minutes",
                'cost': f"${activity['cost']}" if 'cost' in activity else 'Free'
            })
            if 'cost' in activity:
                daily_cost += activity['cost']
        
        return {
            'day_number': day_number,
            'title': template.get('title', f'Day {day_number}'),
            'description': f"Exploring {template.get('title', 'the city')}",
            'activities': activities,
            'daily_total': f"${daily_cost:.2f}",
            'transport': transport_pref or 'Public transport recommended'
        }
    
    def _create_generic_day(
        self,
        day_number: int,
        destination: str,
        interests: List[str]
    ) -> Dict[str, Any]:
        """
        Create a generic day plan when no template exists
        
        Args:
            day_number: Day number
            destination: Destination name
            interests: User interests
            
        Returns:
            Dict: Generic day plan
        """
        activities = []
        
        # Morning
        activities.append({
            'time': '9:00 AM',
            'name': f'Morning exploration in {destination.title()}',
            'details': 'Visit local attractions or landmarks',
            'cost': 'Varies'
        })
        
        # Lunch
        activities.append({
            'time': '12:30 PM',
            'name': 'Lunch',
            'details': 'Try local cuisine',
            'cost': '$15-30'
        })
        
        # Afternoon
        if 'culture' in interests:
            activities.append({
                'time': '2:00 PM',
                'name': 'Visit museum or cultural site',
                'details': 'Explore local history and culture',
                'cost': '$10-20'
            })
        elif 'adventure' in interests:
            activities.append({
                'time': '2:00 PM',
                'name': 'Outdoor activity',
                'details': 'Hiking, biking, or outdoor adventure',
                'cost': '$20-50'
            })
        else:
            activities.append({
                'time': '2:00 PM',
                'name': 'Sightseeing',
                'details': 'Explore popular attractions',
                'cost': '$15-25'
            })
        
        # Evening
        activities.append({
            'time': '7:00 PM',
            'name': 'Dinner',
            'details': 'Enjoy local dining experience',
            'cost': '$25-45'
        })
        
        return {
            'day_number': day_number,
            'title': f'Day {day_number} - {destination.title()}',
            'description': 'Exploring the city',
            'activities': activities,
            'daily_total': '$85-170',
            'notes': 'Itinerary can be customized based on preferences'
        }
    
    def add_activity_to_day(
        self,
        itinerary: Dict[str, Any],
        day_number: int,
        activity: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add an activity to a specific day
        
        Args:
            itinerary: Current itinerary
            day_number: Day to add activity to
            activity: Activity details
            
        Returns:
            Dict: Updated itinerary
        """
        if 0 <= day_number < len(itinerary['days']):
            itinerary['days'][day_number]['activities'].append(activity)
        
        return itinerary
    
    def optimize_itinerary(
        self,
        itinerary: Dict[str, Any],
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Optimize itinerary based on constraints
        
        Args:
            itinerary: Current itinerary
            constraints: Optimization constraints (time, budget, etc.)
            
        Returns:
            Dict: Optimized itinerary
        """
        # This would implement route optimization, time management, etc.
        # For now, return the original
        return itinerary
    
    def export_itinerary(
        self,
        itinerary: Dict[str, Any],
        format: str = 'markdown'
    ) -> str:
        """
        Export itinerary in specified format
        
        Args:
            itinerary: Itinerary to export
            format: Export format (markdown, pdf, json)
            
        Returns:
            str: Formatted itinerary
        """
        if format == 'markdown':
            return self._export_markdown(itinerary)
        elif format == 'json':
            import json
            return json.dumps(itinerary, indent=2)
        else:
            return str(itinerary)
    
    def _export_markdown(self, itinerary: Dict[str, Any]) -> str:
        """
        Export itinerary as markdown
        
        Args:
            itinerary: Itinerary dictionary
            
        Returns:
            str: Markdown formatted itinerary
        """
        output = [f"# {itinerary['title']}\n"]
        output.append(f"**Destination:** {itinerary['destination']}")
        output.append(f"**Duration:** {itinerary['duration']} days\n")
        
        for day in itinerary['days']:
            output.append(f"\n## Day {day['day_number']} - {day['title']}")
            output.append(f"*{day.get('description', '')}*\n")
            
            for activity in day['activities']:
                output.append(f"### {activity['time']} - {activity['name']}")
                output.append(f"{activity.get('details', '')}")
                if 'cost' in activity:
                    output.append(f"**Cost:** {activity['cost']}")
                output.append("")
            
            if 'daily_total' in day:
                output.append(f"**Estimated Daily Cost:** {day['daily_total']}")
            
            if 'notes' in day:
                output.append(f"\n*Note: {day['notes']}*")
            
            output.append("\n---\n")
        
        return "\n".join(output)

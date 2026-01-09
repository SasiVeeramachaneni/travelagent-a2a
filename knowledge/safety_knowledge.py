"""
Safety Knowledge
Contains safety ratings, common scams, emergency contacts, and health tips
"""
from typing import Dict, List, Optional, Any


class SafetyKnowledge:
    """
    Knowledge base for travel safety and health information
    
    This module provides:
    - Safety ratings by destination
    - Common scams and how to avoid them
    - Emergency contact numbers
    - Health tips and vaccinations
    - Safe areas and areas to avoid
    """
    
    def __init__(self):
        """Initialize safety knowledge base"""
        self.safety_data = self._load_safety_data()
        self.health_tips = self._load_health_tips()
    
    def _load_safety_data(self) -> Dict[str, Any]:
        """
        Load safety information database
        
        Structure:
        {
            'destination': {
                'safety_rating': str,
                'emergency_numbers': {...},
                'common_scams': [...],
                'safe_areas': [...],
                'areas_to_avoid': [...],
                'safety_tips': [...]
            }
        }
        """
        return {
            'france': {
                'safety_rating': 'Generally safe, but watch for pickpockets',
                'emergency_numbers': {
                    'police': '17 or 112',
                    'ambulance': '15 or 112',
                    'fire': '18 or 112',
                    'us_embassy': '+33 1 43 12 22 22'
                },
                'common_scams': [
                    {
                        'name': 'Petition scam',
                        'description': 'Someone asks you to sign petition, then demands money',
                        'avoid': 'Politely decline and walk away quickly'
                    },
                    {
                        'name': 'Gold ring scam',
                        'description': 'Person "finds" ring near you, offers to sell it',
                        'avoid': 'Ignore and keep walking'
                    },
                    {
                        'name': 'Friendship bracelet',
                        'description': 'Someone ties bracelet on wrist, demands payment',
                        'avoid': 'Keep hands in pockets near tourist areas'
                    },
                    {
                        'name': 'Metro pickpocketing',
                        'description': 'Thieves work in groups on crowded metro',
                        'avoid': 'Keep bags in front, watch belongings'
                    }
                ],
                'safe_areas': [
                    'Marais (3rd, 4th arrondissements)',
                    'Latin Quarter (5th)',
                    'Saint-Germain-des-Prés (6th)',
                    'Champs-Élysées area (8th)',
                    'Montmartre (18th - daytime)'
                ],
                'areas_to_avoid': [
                    'Northern suburbs at night',
                    'Gare du Nord area at night',
                    'Barbès area',
                    'Château Rouge metro area',
                    'Some parts of 18th, 19th, 20th at night'
                ],
                'safety_tips': [
                    'Use anti-theft bag or money belt',
                    'Don\'t display expensive items',
                    'Be alert in crowded tourist areas',
                    'Keep wallet in front pocket',
                    'Photocopy important documents',
                    'Use official taxis or Uber'
                ]
            },
            'japan': {
                'safety_rating': 'Extremely safe, one of safest countries',
                'emergency_numbers': {
                    'police': '110',
                    'ambulance_fire': '119',
                    'us_embassy': '03-3224-5000',
                    'tourist_helpline': '050-3816-2787 (English)'
                },
                'common_scams': [
                    {
                        'name': 'Overpriced bars',
                        'description': 'Hostess bars with hidden charges',
                        'avoid': 'Check prices before ordering, avoid touts'
                    },
                    {
                        'name': 'JR Pass scam',
                        'description': 'Fake JR Passes sold online',
                        'avoid': 'Buy only from official sources'
                    }
                ],
                'safe_areas': [
                    'Most of Tokyo is very safe',
                    'Shibuya',
                    'Shinjuku',
                    'Asakusa',
                    'Harajuku',
                    'Virtually all areas'
                ],
                'areas_to_avoid': [
                    'Kabukicho late at night (Shinjuku red-light district)',
                    'Roppongi clubs with touts',
                    'Avoid touts outside bars'
                ],
                'safety_tips': [
                    'Crime is very rare',
                    'Lost items often returned',
                    'Still be aware in nightlife areas',
                    'Earthquakes possible - know procedures',
                    'Keep emergency contact card',
                    'Learn some Japanese for emergencies'
                ]
            },
            'usa': {
                'safety_rating': 'Generally safe, varies by area',
                'emergency_numbers': {
                    'emergency': '911 (police, fire, ambulance)',
                    'non_emergency': '311 (in most cities)'
                },
                'common_scams': [
                    {
                        'name': 'Taxi overcharging',
                        'description': 'Some taxis take long routes',
                        'avoid': 'Use Uber/Lyft or check route on maps'
                    },
                    {
                        'name': 'Street performers demanding money',
                        'description': 'Aggressive panhandling',
                        'avoid': 'Say no firmly, don\'t engage'
                    },
                    {
                        'name': 'Fake tickets',
                        'description': 'Counterfeit event tickets',
                        'avoid': 'Buy from official sources only'
                    }
                ],
                'safe_areas': [
                    'Manhattan: Midtown, Upper East/West Side',
                    'Financial District',
                    'Brooklyn: Park Slope, Williamsburg',
                    'Most tourist areas during day'
                ],
                'areas_to_avoid': [
                    'Some parts of Bronx at night',
                    'East New York, Brooklyn',
                    'Certain areas of Harlem at night',
                    'Deserted subway stations late night'
                ],
                'safety_tips': [
                    'Stay aware in crowded areas',
                    'Don\'t flash expensive items',
                    'Use official taxis or ride-shares',
                    'Keep belongings secure on subway',
                    'Know your route before traveling',
                    'Healthcare is expensive - get insurance'
                ]
            },
            'uk': {
                'safety_rating': 'Generally safe, normal precautions',
                'emergency_numbers': {
                    'emergency': '999 (police, fire, ambulance)',
                    'non_emergency_police': '101',
                    'us_embassy': '020 7499 9000'
                },
                'common_scams': [
                    {
                        'name': 'Card skimming at ATMs',
                        'description': 'Devices steal card info',
                        'avoid': 'Use ATMs inside banks, check for devices'
                    },
                    {
                        'name': 'Fake ticket sellers',
                        'description': 'Counterfeit attraction tickets',
                        'avoid': 'Buy from official sources'
                    },
                    {
                        'name': 'Overpriced taxis',
                        'description': 'Unlicensed cabs charge excessive fares',
                        'avoid': 'Use black cabs or licensed minicabs only'
                    }
                ],
                'safe_areas': [
                    'West End',
                    'Covent Garden',
                    'Kensington',
                    'Westminster',
                    'South Bank',
                    'Most of central London'
                ],
                'areas_to_avoid': [
                    'Some areas of East London at night',
                    'Certain parts of South London late',
                    'Avoid isolated areas at night'
                ],
                'safety_tips': [
                    'Watch belongings on tube',
                    'Be aware of pickpockets in tourist areas',
                    'Use licensed taxis only',
                    'Look right when crossing (opposite direction)',
                    'Keep valuables secure',
                    'Use common sense at night'
                ]
            }
        }
    
    def _load_health_tips(self) -> Dict[str, List[Dict[str, str]]]:
        """Load health and vaccination information"""
        return {
            'general': [
                {
                    'topic': 'Travel Insurance',
                    'tip': 'Always get comprehensive travel insurance including medical coverage'
                },
                {
                    'topic': 'Medications',
                    'tip': 'Bring prescription medications in original containers with doctor\'s note'
                },
                {
                    'topic': 'First Aid',
                    'tip': 'Pack basic first aid kit with bandages, pain relievers, anti-diarrheal'
                },
                {
                    'topic': 'Hydration',
                    'tip': 'Stay hydrated, especially in different climates'
                },
                {
                    'topic': 'Jet Lag',
                    'tip': 'Adjust sleep schedule before travel, stay hydrated, get sunlight'
                }
            ],
            'vaccinations': {
                'france': 'Routine vaccinations up to date. No special requirements.',
                'japan': 'Routine vaccinations. Japanese Encephalitis if rural travel.',
                'usa': 'Routine vaccinations up to date.',
                'uk': 'Routine vaccinations up to date.'
            },
            'food_safety': [
                {
                    'tip': 'Wash hands frequently',
                    'priority': 'high'
                },
                {
                    'tip': 'Drink bottled water in developing countries',
                    'priority': 'high'
                },
                {
                    'tip': 'Avoid street food if you have sensitive stomach',
                    'priority': 'medium'
                },
                {
                    'tip': 'Ensure food is properly cooked',
                    'priority': 'high'
                }
            ]
        }
    
    def get_safety_info(
        self,
        destination: str,
        category: Optional[str] = None
    ) -> Any:
        """
        Get safety information for destination
        
        Args:
            destination: Destination name
            category: Specific category or None for all
            
        Returns:
            Safety data
        """
        data = self.safety_data.get(destination.lower())
        if data and category:
            return data.get(category)
        return data
    
    def get_emergency_numbers(self, destination: str) -> Optional[Dict[str, str]]:
        """
        Get emergency contact numbers
        
        Args:
            destination: Destination name
            
        Returns:
            Emergency numbers dict or None
        """
        data = self.safety_data.get(destination.lower())
        if data:
            return data.get('emergency_numbers')
        return None
    
    def get_common_scams(self, destination: str) -> Optional[List[Dict[str, str]]]:
        """
        Get common scams and how to avoid them
        
        Args:
            destination: Destination name
            
        Returns:
            List of scam information
        """
        data = self.safety_data.get(destination.lower())
        if data:
            return data.get('common_scams')
        return None
    
    def get_safe_areas(self, destination: str) -> Optional[List[str]]:
        """
        Get safe areas in destination
        
        Args:
            destination: Destination name
            
        Returns:
            List of safe areas
        """
        data = self.safety_data.get(destination.lower())
        if data:
            return data.get('safe_areas')
        return None
    
    def get_health_tips(self, category: Optional[str] = None) -> Any:
        """
        Get health and medical tips
        
        Args:
            category: Specific category or None for all
            
        Returns:
            Health tips
        """
        if category:
            return self.health_tips.get(category)
        return self.health_tips
    
    def get_vaccination_requirements(self, destination: str) -> Optional[str]:
        """
        Get vaccination requirements
        
        Args:
            destination: Destination name
            
        Returns:
            Vaccination info string
        """
        vacc_data = self.health_tips.get('vaccinations', {})
        return vacc_data.get(destination.lower())

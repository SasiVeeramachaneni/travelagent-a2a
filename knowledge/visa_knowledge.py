"""
Visa Knowledge
Contains visa requirements, passport information, and entry regulations
"""
from typing import Dict, List, Optional, Any


class VisaKnowledge:
    """
    Knowledge base for visa and entry requirements
    
    This module provides:
    - Visa requirements by nationality
    - Passport validity requirements
    - Application processes
    - Processing times
    - Costs and fees
    """
    
    def __init__(self):
        """Initialize visa knowledge base"""
        self.visa_requirements = self._load_visa_requirements()
        self.general_tips = self._load_general_tips()
    
    def _load_visa_requirements(self) -> Dict[str, Any]:
        """
        Load visa requirement database
        
        Structure:
        {
            'destination_country': {
                'origin_region': {
                    'visa_required': bool,
                    'visa_type': str,
                    'duration': str,
                    'cost': float,
                    'processing_time': str,
                    'notes': str
                }
            }
        }
        """
        return {
            'france': {
                'usa': {
                    'visa_required': False,
                    'visa_type': 'Visa-free',
                    'duration': 'Up to 90 days',
                    'cost': 0,
                    'processing_time': 'N/A',
                    'passport_validity': '3 months beyond stay',
                    'notes': 'Part of Schengen area, ETIAS required from 2024'
                },
                'india': {
                    'visa_required': True,
                    'visa_type': 'Schengen Visa',
                    'duration': 'Up to 90 days',
                    'cost': 80,
                    'processing_time': '15-30 days',
                    'passport_validity': '3 months beyond visa expiry',
                    'notes': 'Apply at French consulate or VFS Global'
                },
                'uk': {
                    'visa_required': False,
                    'visa_type': 'Visa-free (post-Brexit)',
                    'duration': 'Up to 90 days',
                    'cost': 0,
                    'processing_time': 'N/A',
                    'passport_validity': '6 months',
                    'notes': 'ETIAS required from 2024'
                }
            },
            'japan': {
                'usa': {
                    'visa_required': False,
                    'visa_type': 'Visa-free',
                    'duration': 'Up to 90 days',
                    'cost': 0,
                    'processing_time': 'N/A',
                    'passport_validity': 'Valid for duration of stay',
                    'notes': 'Tourism or business purposes only'
                },
                'india': {
                    'visa_required': True,
                    'visa_type': 'Tourist Visa',
                    'duration': 'Up to 90 days',
                    'cost': 30,
                    'processing_time': '5-7 business days',
                    'passport_validity': '6 months',
                    'notes': 'Can apply online or at embassy'
                },
                'uk': {
                    'visa_required': False,
                    'visa_type': 'Visa-free',
                    'duration': 'Up to 90 days',
                    'cost': 0,
                    'processing_time': 'N/A',
                    'passport_validity': 'Valid for duration of stay',
                    'notes': 'Tourism or business only'
                }
            },
            'usa': {
                'india': {
                    'visa_required': True,
                    'visa_type': 'B1/B2 Tourist Visa',
                    'duration': 'Up to 6 months',
                    'cost': 160,
                    'processing_time': '30-60 days',
                    'passport_validity': '6 months beyond stay',
                    'notes': 'Interview required at US embassy'
                },
                'uk': {
                    'visa_required': False,
                    'visa_type': 'ESTA (Electronic Authorization)',
                    'duration': 'Up to 90 days',
                    'cost': 21,
                    'processing_time': '72 hours',
                    'passport_validity': 'Valid for duration of stay',
                    'notes': 'Apply online at least 72 hours before travel'
                },
                'eu': {
                    'visa_required': False,
                    'visa_type': 'ESTA (Electronic Authorization)',
                    'duration': 'Up to 90 days',
                    'cost': 21,
                    'processing_time': '72 hours',
                    'passport_validity': 'Valid for duration of stay',
                    'notes': 'Most EU countries eligible for ESTA'
                }
            },
            'uk': {
                'usa': {
                    'visa_required': False,
                    'visa_type': 'Visa-free',
                    'duration': 'Up to 6 months',
                    'cost': 0,
                    'processing_time': 'N/A',
                    'passport_validity': '6 months',
                    'notes': 'ETA required from 2024'
                },
                'india': {
                    'visa_required': True,
                    'visa_type': 'Standard Visitor Visa',
                    'duration': 'Up to 6 months',
                    'cost': 115,
                    'processing_time': '15-20 business days',
                    'passport_validity': '6 months beyond stay',
                    'notes': 'Apply online, may require biometrics'
                },
                'eu': {
                    'visa_required': False,
                    'visa_type': 'Visa-free',
                    'duration': 'Up to 6 months',
                    'cost': 0,
                    'processing_time': 'N/A',
                    'passport_validity': '6 months',
                    'notes': 'Post-Brexit rules apply'
                }
            }
        }
    
    def _load_general_tips(self) -> Dict[str, List[str]]:
        """Load general visa and travel document tips"""
        return {
            'before_applying': [
                'Check if you need a visa well in advance (2-3 months)',
                'Ensure passport is valid for required period',
                'Have blank pages in passport (usually 2-3 required)',
                'Gather required documents (photos, bank statements, etc.)',
                'Book refundable flights for visa application',
                'Get travel insurance'
            ],
            'application_tips': [
                'Apply as early as possible',
                'Double-check all information before submitting',
                'Keep copies of all documents',
                'Be honest in your application',
                'Provide comprehensive travel itinerary',
                'Show proof of funds and ties to home country'
            ],
            'documents_needed': [
                'Valid passport',
                'Passport-sized photos (specific requirements)',
                'Completed visa application form',
                'Proof of accommodation',
                'Flight itinerary or booking',
                'Bank statements (3-6 months)',
                'Travel insurance',
                'Employment letter or proof of income',
                'Purpose of visit documentation'
            ],
            'at_immigration': [
                'Have all documents ready and accessible',
                'Be polite and answer questions clearly',
                'Have return ticket confirmation',
                'Know your accommodation address',
                'Declare any restricted items',
                'Keep visa/entry stamp safe'
            ]
        }
    
    def get_visa_requirements(
        self,
        origin: str,
        destination: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get visa requirements for a specific route
        
        Args:
            origin: Origin country/region
            destination: Destination country
            
        Returns:
            Visa requirement details or None
        """
        dest_country = destination.lower()
        origin_region = origin.lower()
        
        if dest_country in self.visa_requirements:
            return self.visa_requirements[dest_country].get(origin_region)
        
        return None
    
    def is_visa_required(self, origin: str, destination: str) -> bool:
        """
        Check if visa is required
        
        Args:
            origin: Origin country/region
            destination: Destination country
            
        Returns:
            True if visa required, False otherwise
        """
        requirements = self.get_visa_requirements(origin, destination)
        if requirements:
            return requirements.get('visa_required', True)
        return True  # Assume visa required if no data
    
    def get_visa_cost(self, origin: str, destination: str) -> Optional[float]:
        """
        Get visa cost
        
        Args:
            origin: Origin country/region
            destination: Destination country
            
        Returns:
            Visa cost or None
        """
        requirements = self.get_visa_requirements(origin, destination)
        if requirements:
            return requirements.get('cost')
        return None
    
    def get_processing_time(self, origin: str, destination: str) -> Optional[str]:
        """
        Get visa processing time
        
        Args:
            origin: Origin country/region
            destination: Destination country
            
        Returns:
            Processing time string or None
        """
        requirements = self.get_visa_requirements(origin, destination)
        if requirements:
            return requirements.get('processing_time')
        return None
    
    def get_general_tips(self, category: Optional[str] = None) -> Any:
        """
        Get general visa tips
        
        Args:
            category: Specific category or None for all
            
        Returns:
            Tips for category or all tips
        """
        if category:
            return self.general_tips.get(category)
        return self.general_tips
    
    def get_passport_validity_requirement(
        self,
        origin: str,
        destination: str
    ) -> Optional[str]:
        """
        Get passport validity requirement
        
        Args:
            origin: Origin country/region
            destination: Destination country
            
        Returns:
            Validity requirement string or None
        """
        requirements = self.get_visa_requirements(origin, destination)
        if requirements:
            return requirements.get('passport_validity')
        return '6 months'  # Common default

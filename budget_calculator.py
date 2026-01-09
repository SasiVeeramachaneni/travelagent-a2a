"""
Budget Calculator Service
Calculates comprehensive trip costs with detailed breakdowns
"""
from typing import Dict, List, Optional, Any
from datetime import datetime


class BudgetCalculator:
    """
    Service for calculating trip budgets and cost breakdowns
    """
    
    def __init__(self):
        """Initialize budget calculator"""
        self.pricing_data = self._load_pricing_data()
    
    def _load_pricing_data(self) -> Dict[str, Any]:
        """
        Load pricing data for different destinations and categories
        
        Returns:
            Dict: Pricing information database
        """
        return {
            'paris': {
                'flights': {
                    'from_india': {'budget': 650, 'moderate': 850, 'luxury': 1500},
                    'from_usa': {'budget': 500, 'moderate': 750, 'luxury': 2000},
                    'from_asia': {'budget': 550, 'moderate': 800, 'luxury': 1800}
                },
                'accommodation_per_night': {
                    'hostel': 35,
                    'budget_hotel': 75,
                    'hotel': 150,
                    'vacation_rental': 120,
                    'luxury': 350
                },
                'meals_per_day': {
                    'budget': 35,
                    'moderate': 60,
                    'luxury': 120
                },
                'local_transport_per_day': {
                    'public_transport': 8,
                    'rental_car': 50,
                    'ride_sharing': 25,
                    'walking': 0,
                    'mix': 15
                },
                'activities_per_day': {
                    'budget': 15,
                    'moderate': 35,
                    'luxury': 75
                }
            },
            'tokyo': {
                'flights': {
                    'from_india': {'budget': 550, 'moderate': 750, 'luxury': 1400},
                    'from_usa': {'budget': 700, 'moderate': 1000, 'luxury': 3000},
                    'from_europe': {'budget': 600, 'moderate': 900, 'luxury': 2500}
                },
                'accommodation_per_night': {
                    'hostel': 30,
                    'budget_hotel': 60,
                    'hotel': 120,
                    'vacation_rental': 100,
                    'luxury': 300
                },
                'meals_per_day': {
                    'budget': 30,
                    'moderate': 50,
                    'luxury': 100
                },
                'local_transport_per_day': {
                    'public_transport': 10,
                    'rental_car': 70,
                    'ride_sharing': 30,
                    'walking': 0,
                    'mix': 18
                },
                'activities_per_day': {
                    'budget': 12,
                    'moderate': 30,
                    'luxury': 70
                }
            },
            'new york': {
                'flights': {
                    'from_india': {'budget': 750, 'moderate': 1000, 'luxury': 2500},
                    'from_europe': {'budget': 400, 'moderate': 650, 'luxury': 2000},
                    'from_asia': {'budget': 700, 'moderate': 950, 'luxury': 2200}
                },
                'accommodation_per_night': {
                    'hostel': 50,
                    'budget_hotel': 120,
                    'hotel': 200,
                    'vacation_rental': 160,
                    'luxury': 450
                },
                'meals_per_day': {
                    'budget': 45,
                    'moderate': 80,
                    'luxury': 150
                },
                'local_transport_per_day': {
                    'public_transport': 12,
                    'rental_car': 80,
                    'ride_sharing': 35,
                    'walking': 0,
                    'mix': 20
                },
                'activities_per_day': {
                    'budget': 20,
                    'moderate': 45,
                    'luxury': 100
                }
            }
        }
    
    def calculate_total_cost(
        self,
        origin: Optional[str],
        destination: str,
        duration: int,
        travelers: int = 1,
        budget_level: str = 'moderate',
        accommodation_type: Optional[str] = None,
        activities: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive trip cost with detailed breakdown
        
        Args:
            origin: Origin city/region
            destination: Destination city
            duration: Number of days
            travelers: Number of travelers
            budget_level: Budget level (budget, moderate, luxury)
            accommodation_type: Type of accommodation
            activities: List of planned activities
            
        Returns:
            Dict: Detailed cost breakdown
        """
        destination_key = destination.lower()
        
        if destination_key not in self.pricing_data:
            return self._calculate_generic_cost(
                duration, travelers, budget_level
            )
        
        dest_pricing = self.pricing_data[destination_key]
        
        # Calculate flights
        flight_cost = self._calculate_flight_cost(
            origin, destination_key, budget_level, dest_pricing
        ) * travelers
        
        # Calculate accommodation
        accommodation_cost = self._calculate_accommodation_cost(
            destination_key, duration, accommodation_type, budget_level, dest_pricing
        )
        
        # Calculate meals
        meals_cost = self._calculate_meals_cost(
            destination_key, duration, travelers, budget_level, dest_pricing
        )
        
        # Calculate local transport
        transport_cost = self._calculate_transport_cost(
            destination_key, duration, travelers, budget_level, dest_pricing
        )
        
        # Calculate activities
        activities_cost = self._calculate_activities_cost(
            destination_key, duration, travelers, budget_level, activities, dest_pricing
        )
        
        # Calculate miscellaneous (15% buffer)
        subtotal = (flight_cost + accommodation_cost + meals_cost + 
                   transport_cost + activities_cost)
        miscellaneous = subtotal * 0.15
        
        total = subtotal + miscellaneous
        
        return {
            'currency': '$',
            'flights': flight_cost,
            'accommodation': accommodation_cost,
            'local_transport': transport_cost,
            'meals': meals_cost,
            'activities': activities_cost,
            'miscellaneous': miscellaneous,
            'subtotal': subtotal,
            'total': total,
            'breakdown': {
                'flights_detail': f'Round-trip for {travelers} traveler(s)',
                'accommodation_detail': f'{duration - 1} nights',
                'meals_detail': f'{duration} days × {travelers} traveler(s)',
                'transport_detail': f'{duration} days of local transport',
                'activities_detail': 'Attractions, tours, and experiences',
                'misc_detail': '15% buffer for tips, shopping, emergencies'
            },
            'per_person': total / travelers if travelers > 1 else total
        }
    
    def _calculate_flight_cost(
        self,
        origin: Optional[str],
        destination: str,
        budget_level: str,
        dest_pricing: Dict[str, Any]
    ) -> float:
        """Calculate flight cost"""
        if not origin:
            # Default to moderate pricing if origin not specified
            return 800
        
        origin_region = self._get_region_from_origin(origin)
        flights = dest_pricing.get('flights', {})
        
        if origin_region in flights:
            return flights[origin_region].get(budget_level, 800)
        
        # Default estimate
        return {'budget': 600, 'moderate': 900, 'luxury': 2000}[budget_level]
    
    def _calculate_accommodation_cost(
        self,
        destination: str,
        duration: int,
        accommodation_type: Optional[str],
        budget_level: str,
        dest_pricing: Dict[str, Any]
    ) -> float:
        """Calculate accommodation cost"""
        nights = duration - 1  # Usually one less night than days
        
        acc_pricing = dest_pricing.get('accommodation_per_night', {})
        
        # Determine accommodation type from budget level if not specified
        if not accommodation_type:
            type_map = {
                'budget': 'budget_hotel',
                'moderate': 'hotel',
                'luxury': 'luxury'
            }
            accommodation_type = type_map[budget_level]
        
        # Map accommodation preference to pricing key
        type_mapping = {
            'hostel': 'hostel',
            'budget_hotel': 'budget_hotel',
            'hotel': 'hotel',
            'vacation_rental': 'vacation_rental',
            'resort': 'luxury',
            'luxury': 'luxury'
        }
        
        pricing_key = type_mapping.get(accommodation_type, 'hotel')
        per_night = acc_pricing.get(pricing_key, 100)
        
        return per_night * nights
    
    def _calculate_meals_cost(
        self,
        destination: str,
        duration: int,
        travelers: int,
        budget_level: str,
        dest_pricing: Dict[str, Any]
    ) -> float:
        """Calculate meals cost"""
        meals_pricing = dest_pricing.get('meals_per_day', {})
        per_day = meals_pricing.get(budget_level, 50)
        
        return per_day * duration * travelers
    
    def _calculate_transport_cost(
        self,
        destination: str,
        duration: int,
        travelers: int,
        budget_level: str,
        dest_pricing: Dict[str, Any]
    ) -> float:
        """Calculate local transportation cost"""
        transport_pricing = dest_pricing.get('local_transport_per_day', {})
        
        # Default to mix if not specified
        per_day = transport_pricing.get('mix', 15)
        
        return per_day * duration * travelers
    
    def _calculate_activities_cost(
        self,
        destination: str,
        duration: int,
        travelers: int,
        budget_level: str,
        activities: Optional[List[str]],
        dest_pricing: Dict[str, Any]
    ) -> float:
        """Calculate activities and attractions cost"""
        activities_pricing = dest_pricing.get('activities_per_day', {})
        per_day = activities_pricing.get(budget_level, 30)
        
        # If specific activities provided, could calculate more accurately
        # For now, use per-day estimate
        return per_day * duration * travelers
    
    def _get_region_from_origin(self, origin: str) -> str:
        """
        Determine region from origin city/country
        
        Args:
            origin: Origin location
            
        Returns:
            str: Region identifier
        """
        origin_lower = origin.lower()
        
        if any(country in origin_lower for country in ['india', 'delhi', 'mumbai', 'bangalore']):
            return 'from_india'
        elif any(country in origin_lower for country in ['usa', 'america', 'new york', 'los angeles']):
            return 'from_usa'
        elif any(country in origin_lower for country in ['japan', 'china', 'korea', 'singapore', 'tokyo']):
            return 'from_asia'
        elif any(country in origin_lower for country in ['uk', 'france', 'germany', 'europe', 'london', 'paris']):
            return 'from_europe'
        else:
            return 'from_asia'  # Default
    
    def _calculate_generic_cost(
        self,
        duration: int,
        travelers: int,
        budget_level: str
    ) -> Dict[str, Any]:
        """
        Calculate generic cost estimate when destination not in database
        
        Args:
            duration: Number of days
            travelers: Number of travelers
            budget_level: Budget level
            
        Returns:
            Dict: Generic cost breakdown
        """
        # Generic estimates
        estimates = {
            'budget': {
                'flight': 600,
                'accommodation_per_night': 60,
                'meals_per_day': 35,
                'transport_per_day': 12,
                'activities_per_day': 15
            },
            'moderate': {
                'flight': 900,
                'accommodation_per_night': 130,
                'meals_per_day': 60,
                'transport_per_day': 20,
                'activities_per_day': 35
            },
            'luxury': {
                'flight': 2000,
                'accommodation_per_night': 300,
                'meals_per_day': 120,
                'transport_per_day': 40,
                'activities_per_day': 80
            }
        }
        
        est = estimates[budget_level]
        nights = duration - 1
        
        flight_cost = est['flight'] * travelers
        accommodation_cost = est['accommodation_per_night'] * nights
        meals_cost = est['meals_per_day'] * duration * travelers
        transport_cost = est['transport_per_day'] * duration * travelers
        activities_cost = est['activities_per_day'] * duration * travelers
        
        subtotal = (flight_cost + accommodation_cost + meals_cost + 
                   transport_cost + activities_cost)
        miscellaneous = subtotal * 0.15
        total = subtotal + miscellaneous
        
        return {
            'currency': '$',
            'flights': flight_cost,
            'accommodation': accommodation_cost,
            'local_transport': transport_cost,
            'meals': meals_cost,
            'activities': activities_cost,
            'miscellaneous': miscellaneous,
            'subtotal': subtotal,
            'total': total,
            'per_person': total / travelers if travelers > 1 else total,
            'note': 'Estimated costs - actual prices may vary'
        }
    
    def compare_budget_levels(
        self,
        origin: Optional[str],
        destination: str,
        duration: int,
        travelers: int = 1
    ) -> Dict[str, Dict[str, Any]]:
        """
        Compare costs across different budget levels
        
        Args:
            origin: Origin location
            destination: Destination
            duration: Trip duration
            travelers: Number of travelers
            
        Returns:
            Dict: Comparison of budget levels
        """
        comparison = {}
        
        for budget_level in ['budget', 'moderate', 'luxury']:
            comparison[budget_level] = self.calculate_total_cost(
                origin, destination, duration, travelers, budget_level
            )
        
        return comparison
    
    def optimize_budget(
        self,
        target_budget: float,
        current_breakdown: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Suggest optimizations to meet target budget
        
        Args:
            target_budget: Target budget amount
            current_breakdown: Current cost breakdown
            
        Returns:
            Dict: Optimization suggestions
        """
        current_total = current_breakdown.get('total', 0)
        difference = current_total - target_budget
        
        suggestions = {
            'target_budget': target_budget,
            'current_total': current_total,
            'difference': difference,
            'recommendations': []
        }
        
        if difference > 0:
            # Over budget - provide cost-cutting suggestions
            suggestions['status'] = 'over_budget'
            suggestions['recommendations'] = [
                'Consider traveling during off-peak season',
                'Look for budget-friendly accommodation options',
                'Use public transportation instead of taxis',
                'Cook some meals instead of dining out',
                'Book flights in advance for better deals',
                'Choose free or low-cost activities'
            ]
        else:
            # Under budget - suggest upgrades
            suggestions['status'] = 'under_budget'
            suggestions['recommendations'] = [
                'Upgrade to better accommodation',
                'Add premium activities or tours',
                'Include special dining experiences',
                'Consider extending your trip',
                'Add day trips to nearby destinations'
            ]
        
        return suggestions
    
    def calculate_daily_budget(
        self,
        total_budget: float,
        duration: int,
        fixed_costs: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Calculate daily spending budget after fixed costs
        
        Args:
            total_budget: Total trip budget
            duration: Trip duration
            fixed_costs: Fixed costs (flights, accommodation)
            
        Returns:
            Dict: Daily budget breakdown
        """
        total_fixed = sum(fixed_costs.values())
        remaining = total_budget - total_fixed
        daily_budget = remaining / duration
        
        return {
            'total_budget': total_budget,
            'fixed_costs': fixed_costs,
            'total_fixed': total_fixed,
            'remaining_for_daily': remaining,
            'daily_budget': daily_budget,
            'recommended_allocation': {
                'meals': daily_budget * 0.45,
                'activities': daily_budget * 0.35,
                'transport': daily_budget * 0.15,
                'miscellaneous': daily_budget * 0.05
            }
        }

"""
Data models for the travel agent
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class BudgetLevel(Enum):
    """Budget level enumeration"""
    BUDGET = "budget"
    MODERATE = "moderate"
    LUXURY = "luxury"


class AccommodationType(Enum):
    """Accommodation type enumeration"""
    HOSTEL = "hostel"
    BUDGET_HOTEL = "budget_hotel"
    HOTEL = "hotel"
    VACATION_RENTAL = "vacation_rental"
    RESORT = "resort"
    LUXURY = "luxury"


class TransportMode(Enum):
    """Local transportation mode enumeration"""
    PUBLIC_TRANSPORT = "public_transport"
    RENTAL_CAR = "rental_car"
    RIDE_SHARING = "ride_sharing"
    WALKING = "walking"
    BIKE = "bike"
    MIX = "mix"


@dataclass
class TripPreferences:
    """User's trip preferences"""
    destination: str
    origin: Optional[str] = None
    duration: Optional[int] = None
    travelers: int = 1
    budget: Optional[float] = None
    budget_level: BudgetLevel = BudgetLevel.MODERATE
    interests: List[str] = field(default_factory=list)
    accommodation_type: Optional[AccommodationType] = None
    transport_preference: Optional[TransportMode] = None
    departure_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    flexibility: str = "moderate"  # flexible, moderate, fixed
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'destination': self.destination,
            'origin': self.origin,
            'duration': self.duration,
            'travelers': self.travelers,
            'budget': self.budget,
            'budget_level': self.budget_level.value if isinstance(self.budget_level, BudgetLevel) else self.budget_level,
            'interests': self.interests,
            'accommodation_type': self.accommodation_type.value if self.accommodation_type else None,
            'transport_preference': self.transport_preference.value if self.transport_preference else None,
            'departure_date': self.departure_date.isoformat() if self.departure_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'flexibility': self.flexibility
        }


@dataclass
class Activity:
    """Activity information"""
    name: str
    time: str
    duration: int  # in minutes
    cost: Optional[float] = None
    location: Optional[str] = None
    description: Optional[str] = None
    booking_required: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'time': self.time,
            'duration': self.duration,
            'cost': self.cost,
            'location': self.location,
            'description': self.description,
            'booking_required': self.booking_required
        }


@dataclass
class DayPlan:
    """Single day plan in itinerary"""
    day_number: int
    title: str
    description: str
    activities: List[Activity] = field(default_factory=list)
    daily_total: Optional[float] = None
    notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'day_number': self.day_number,
            'title': self.title,
            'description': self.description,
            'activities': [a.to_dict() for a in self.activities],
            'daily_total': self.daily_total,
            'notes': self.notes
        }


@dataclass
class Itinerary:
    """Complete trip itinerary"""
    title: str
    destination: str
    duration: int
    days: List[DayPlan] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'title': self.title,
            'destination': self.destination,
            'duration': self.duration,
            'days': [d.to_dict() for d in self.days],
            'created_at': self.created_at.isoformat()
        }


@dataclass
class BudgetBreakdown:
    """Budget breakdown"""
    flights: float
    accommodation: float
    meals: float
    local_transport: float
    activities: float
    miscellaneous: float
    total: float
    currency: str = "$"
    per_person: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'currency': self.currency,
            'flights': self.flights,
            'accommodation': self.accommodation,
            'meals': self.meals,
            'local_transport': self.local_transport,
            'activities': self.activities,
            'miscellaneous': self.miscellaneous,
            'total': self.total,
            'per_person': self.per_person
        }


@dataclass
class Destination:
    """Destination information"""
    name: str
    country: str
    description: Optional[str] = None
    best_months: List[str] = field(default_factory=list)
    avg_daily_budget: Optional[Dict[str, float]] = None
    top_attractions: List[str] = field(default_factory=list)
    safety_rating: Optional[float] = None
    visa_info: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'country': self.country,
            'description': self.description,
            'best_months': self.best_months,
            'avg_daily_budget': self.avg_daily_budget,
            'top_attractions': self.top_attractions,
            'safety_rating': self.safety_rating,
            'visa_info': self.visa_info
        }

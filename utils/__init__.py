"""Utilities package for travel agent

This package contains:
- models: Data classes for trip preferences, activities, itineraries
- helpers: Utility functions for parsing and formatting
"""
from .models import (
    BudgetLevel,
    AccommodationType,
    TransportMode,
    TripPreferences,
    Activity
)
from .helpers import (
    parse_budget_from_text,
    parse_duration_from_text,
    format_currency,
    calculate_trip_days
)

__all__ = [
    'BudgetLevel',
    'AccommodationType',
    'TransportMode',
    'TripPreferences',
    'Activity',
    'parse_budget_from_text',
    'parse_duration_from_text',
    'format_currency',
    'calculate_trip_days'
]

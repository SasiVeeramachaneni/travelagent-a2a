"""
Helper utilities for the travel agent
"""
from typing import Dict, List, Any, Optional
import re
from datetime import datetime, timedelta


def parse_budget_from_text(text: str) -> Optional[float]:
    """
    Parse budget amount from text
    
    Args:
        text: Text containing budget information
        
    Returns:
        Optional[float]: Parsed budget amount or None
    """
    # Match patterns like $5000, 5000 USD, INR 100000, etc.
    patterns = [
        r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',  # $5000 or $5,000.00
        r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:USD|usd|dollars?)',  # 5000 USD
        r'(?:INR|Rs\.?|₹)\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',  # INR 100000
        r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:INR|rupees?)',  # 100000 INR
        r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:EUR|euros?|€)',  # 5000 EUR
        r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:GBP|pounds?|£)',  # 5000 GBP
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            amount_str = match.group(1).replace(',', '')
            return float(amount_str)
    
    return None


def parse_duration_from_text(text: str) -> Optional[int]:
    """
    Parse trip duration from text
    
    Args:
        text: Text containing duration information
        
    Returns:
        Optional[int]: Duration in days or None
    """
    patterns = [
        (r'(\d+)\s*days?', 1),
        (r'(\d+)\s*weeks?', 7),
        (r'(\d+)\s*nights?', 1),  # nights + 1 = days
    ]
    
    for pattern, multiplier in patterns:
        match = re.search(pattern, text.lower())
        if match:
            value = int(match.group(1))
            if 'night' in pattern:
                return value + 1
            return value * multiplier
    
    return None


def format_currency(amount: float, currency: str = "$") -> str:
    """
    Format currency amount
    
    Args:
        amount: Amount to format
        currency: Currency symbol
        
    Returns:
        str: Formatted currency string
    """
    return f"{currency}{amount:,.2f}"


def calculate_trip_days(start_date: datetime, end_date: datetime) -> int:
    """
    Calculate number of days in a trip
    
    Args:
        start_date: Trip start date
        end_date: Trip end date
        
    Returns:
        int: Number of days
    """
    return (end_date - start_date).days + 1


def validate_trip_preferences(preferences: Dict[str, Any]) -> List[str]:
    """
    Validate trip preferences and return list of errors
    
    Args:
        preferences: Trip preferences dictionary
        
    Returns:
        List[str]: List of validation errors
    """
    errors = []
    
    if not preferences.get('destination'):
        errors.append("Destination is required")
    
    if preferences.get('duration') and preferences['duration'] < 1:
        errors.append("Duration must be at least 1 day")
    
    if preferences.get('travelers') and preferences['travelers'] < 1:
        errors.append("Number of travelers must be at least 1")
    
    if preferences.get('budget') and preferences['budget'] < 0:
        errors.append("Budget must be a positive number")
    
    return errors


def extract_city_from_text(text: str) -> Optional[str]:
    """
    Extract city name from text
    
    Args:
        text: Text potentially containing city name
        
    Returns:
        Optional[str]: Extracted city name or None
    """
    # Common patterns for city mentions
    patterns = [
        r'(?:to|in|visit|visiting)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:trip|vacation|holiday)',
        r'traveling to\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    return None


def get_season_from_month(month: int) -> str:
    """
    Get season from month number
    
    Args:
        month: Month number (1-12)
        
    Returns:
        str: Season name
    """
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "fall"


def calculate_days_until_trip(departure_date: datetime) -> int:
    """
    Calculate days until trip
    
    Args:
        departure_date: Trip departure date
        
    Returns:
        int: Days until trip
    """
    today = datetime.now()
    return (departure_date - today).days


def format_date_range(start_date: datetime, end_date: datetime) -> str:
    """
    Format date range for display
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        str: Formatted date range
    """
    if start_date.year == end_date.year:
        if start_date.month == end_date.month:
            return f"{start_date.strftime('%B %d')} - {end_date.strftime('%d, %Y')}"
        else:
            return f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}"
    else:
        return f"{start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}"


def estimate_optimal_booking_time(departure_date: datetime) -> Dict[str, Any]:
    """
    Estimate optimal time to book for best prices
    
    Args:
        departure_date: Trip departure date
        
    Returns:
        Dict: Booking recommendations
    """
    today = datetime.now()
    days_until = (departure_date - today).days
    
    if days_until < 14:
        return {
            'status': 'urgent',
            'message': 'Book immediately! Prices increase close to departure.',
            'recommendation': 'Book flights and accommodation ASAP'
        }
    elif days_until < 30:
        return {
            'status': 'soon',
            'message': 'Book within the next week for better rates.',
            'recommendation': 'Start booking major items now'
        }
    elif days_until < 60:
        return {
            'status': 'good_time',
            'message': 'Good time to start booking.',
            'recommendation': 'Monitor prices and book when you see good deals'
        }
    else:
        return {
            'status': 'early',
            'message': 'You have time, but can start planning.',
            'recommendation': 'Set up price alerts and research options'
        }


def split_into_paragraphs(text: str, max_length: int = 500) -> List[str]:
    """
    Split text into paragraphs for better readability
    
    Args:
        text: Text to split
        max_length: Maximum length per paragraph
        
    Returns:
        List[str]: List of paragraphs
    """
    sentences = text.split('. ')
    paragraphs = []
    current = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence)
        if current_length + sentence_length > max_length and current:
            paragraphs.append('. '.join(current) + '.')
            current = [sentence]
            current_length = sentence_length
        else:
            current.append(sentence)
            current_length += sentence_length
    
    if current:
        paragraphs.append('. '.join(current) + ('.' if not current[-1].endswith('.') else ''))
    
    return paragraphs


def merge_dictionaries(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple dictionaries
    
    Args:
        *dicts: Dictionaries to merge
        
    Returns:
        Dict: Merged dictionary
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


def sanitize_user_input(text: str) -> str:
    """
    Sanitize user input by removing potentially harmful content
    
    Args:
        text: User input text
        
    Returns:
        str: Sanitized text
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Trim
    text = text.strip()
    
    return text


def generate_trip_id(destination: str, start_date: datetime) -> str:
    """
    Generate a unique trip ID
    
    Args:
        destination: Trip destination
        start_date: Trip start date
        
    Returns:
        str: Trip ID
    """
    dest_code = destination[:3].upper()
    date_code = start_date.strftime('%Y%m%d')
    return f"TRIP-{dest_code}-{date_code}"

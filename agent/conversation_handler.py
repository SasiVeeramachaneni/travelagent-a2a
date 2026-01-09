"""
Conversation Handler
Manages user interactions, intent parsing, and response formatting
"""
from typing import Dict, List, Optional, Any
import re


class ConversationHandler:
    """
    Handles conversation flow, intent detection, and response formatting
    for the travel agent
    """
    
    def __init__(self):
        """Initialize conversation handler"""
        self.conversation_history: List[Dict[str, str]] = []
        self.current_phase = "greeting"
        
    def greet_user(self) -> str:
        """
        Generate a warm greeting for the user
        
        Returns:
            str: Greeting message
        """
        return (
            "Hello! 👋 I'm your intelligent travel agent, ready to help you plan "
            "an amazing trip! Whether you're looking for adventure, relaxation, "
            "cultural experiences, or something in between, I'm here to make your "
            "travel dreams a reality.\n\n"
            "Where would you like to go? 🌍"
        )
    
    def parse_intent(self, message: str) -> str:
        """
        Parse user message to determine intent
        
        Args:
            message: User's message
            
        Returns:
            str: Detected intent
        """
        message_lower = message.lower()
        
        # Intent patterns
        if any(word in message_lower for word in ['plan', 'planning', 'trip to', 'visit', 'going to']):
            return "plan_trip"
        elif any(word in message_lower for word in ['recommend', 'suggest', 'what to do', 'what should']):
            return "get_recommendations"
        elif any(word in message_lower for word in ['itinerary', 'schedule', 'day by day', 'daily plan']):
            return "create_itinerary"
        elif any(word in message_lower for word in ['budget', 'cost', 'price', 'how much', 'expensive']):
            return "calculate_budget"
        elif any(word in message_lower for word in ['book', 'booking', 'reserve', 'reservation']):
            return "booking_assistance"
        elif any(word in message_lower for word in ['visa', 'passport', 'insurance', 'safety', 'emergency']):
            return "travel_support"
        else:
            return "general_inquiry"
    
    def extract_context(self, message: str, current_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant context from user message
        
        Args:
            message: User's message
            current_context: Current conversation context
            
        Returns:
            Dict: Updated context
        """
        context = current_context.copy()
        message_lower = message.lower()
        
        # Extract destination
        destinations = [
            'paris', 'tokyo', 'new york', 'london', 'rome',
            'barcelona', 'dubai', 'singapore', 'sydney', 'bali',
            'amsterdam', 'berlin', 'lisbon', 'prague', 'bangkok'
        ]
        for dest in destinations:
            if dest in message_lower:
                context['destination'] = dest.title()
                break
        
        # Extract origin
        origin_patterns = [
            r'from\s+([a-zA-Z\s]+?)(?:\s+to\s|\s*$|,)',
            r'traveling\s+from\s+([a-zA-Z\s]+)',
            r'leaving\s+from\s+([a-zA-Z\s]+)'
        ]
        for pattern in origin_patterns:
            match = re.search(pattern, message_lower)
            if match:
                origin = match.group(1).strip().title()
                if origin and origin.lower() not in destinations:
                    context['origin'] = origin
                break
        
        # Extract budget amount
        budget_patterns = [
            r'\$\s*(\d+(?:,\d{3})*)',
            r'(\d+(?:,\d{3})*)\s*(?:dollars?|usd)',
            r'budget\s+(?:of\s+)?\$?\s*(\d+(?:,\d{3})*)'
        ]
        for pattern in budget_patterns:
            match = re.search(pattern, message_lower)
            if match:
                context['budget'] = float(match.group(1).replace(',', ''))
                break
        
        # Extract budget level
        if 'budget' in message_lower or 'cheap' in message_lower:
            context['budget_level'] = 'budget'
        elif 'luxury' in message_lower or 'premium' in message_lower or 'high-end' in message_lower:
            context['budget_level'] = 'luxury'
        elif 'moderate' in message_lower or 'mid-range' in message_lower:
            context['budget_level'] = 'moderate'
        
        # Extract duration patterns
        duration_patterns = [
            (r'(\d+)\s*days?', 'days'),
            (r'(\d+)\s*weeks?', 'weeks'),
            (r'(\d+)\s*nights?', 'nights')
        ]
        
        for pattern, unit in duration_patterns:
            match = re.search(pattern, message_lower)
            if match:
                value = int(match.group(1))
                if unit == 'weeks':
                    value *= 7
                elif unit == 'nights':
                    value += 1  # Convert nights to days
                context['duration'] = value
                break
        
        # Extract number of travelers
        traveler_match = re.search(r'(\d+)\s*(?:people|person|traveler|passenger)', message_lower)
        if traveler_match:
            context['travelers'] = int(traveler_match.group(1))
        
        # Extract accommodation preferences
        if 'hotel' in message_lower:
            context['accommodation_type'] = 'hotel'
        elif 'hostel' in message_lower:
            context['accommodation_type'] = 'hostel'
        elif 'airbnb' in message_lower or 'vacation rental' in message_lower:
            context['accommodation_type'] = 'vacation_rental'
        elif 'resort' in message_lower:
            context['accommodation_type'] = 'resort'
        
        # Extract transport preferences
        if 'public transport' in message_lower or 'metro' in message_lower or 'bus' in message_lower:
            context['local_transport'] = 'public_transport'
        elif 'rental car' in message_lower or 'car rental' in message_lower:
            context['local_transport'] = 'rental_car'
        elif 'taxi' in message_lower or 'uber' in message_lower or 'ride' in message_lower:
            context['local_transport'] = 'ride_sharing'
        elif 'walk' in message_lower or 'walking' in message_lower:
            context['local_transport'] = 'walking'
        
        # Extract interests
        interests = []
        interest_keywords = {
            'culture': ['museum', 'culture', 'historical', 'history', 'art'],
            'adventure': ['adventure', 'hiking', 'outdoor', 'nature', 'trek'],
            'food': ['food', 'restaurant', 'dining', 'cuisine', 'culinary'],
            'relaxation': ['relax', 'beach', 'spa', 'peaceful', 'quiet'],
            'nightlife': ['nightlife', 'bar', 'club', 'party'],
            'shopping': ['shopping', 'mall', 'market', 'boutique']
        }
        
        for interest, keywords in interest_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                interests.append(interest)
        
        if interests:
            context['interests'] = interests
        
        return context
    
    def get_required_information(self) -> List[str]:
        """
        Get list of required information for trip planning
        
        Returns:
            List[str]: Required information fields
        """
        return [
            'destination',
            'origin',
            'duration',
            'budget',
            'travelers',
            'travel_dates',
            'budget_level',
            'interests'
        ]
    
    def check_missing_information(
        self, 
        context: Dict[str, Any], 
        required: List[str]
    ) -> List[str]:
        """
        Check what required information is missing from context
        
        Args:
            context: Current context
            required: List of required fields
            
        Returns:
            List[str]: Missing fields
        """
        # Prioritize essential fields
        essential = ['destination', 'duration', 'budget']
        missing_essential = [field for field in essential if field not in context]
        
        if missing_essential:
            return missing_essential
        
        return [field for field in required if field not in context]
    
    def ask_for_information(self, field: str) -> str:
        """
        Generate question to ask for missing information
        
        Args:
            field: The information field to ask about
            
        Returns:
            str: Question to ask user
        """
        questions = {
            'destination': "Where would you like to travel to? 🌍",
            'origin': "Where will you be traveling from? (City/Airport) ✈️",
            'duration': "How many days do you have for this trip? 📅",
            'budget': (
                "What's your budget for this trip? 💰\n"
                "You can tell me:\n"
                "• A specific amount (e.g., '$5000')\n"
                "• A budget level: Budget-Friendly 💰 | Moderate 💵 | Luxury 💎"
            ),
            'travelers': "How many people will be traveling? 👥",
            'travel_dates': (
                "When are you planning to travel? 📅\n"
                "Please provide your preferred dates or let me know if you're flexible."
            ),
            'budget_level': (
                "What's your preferred budget level? 💰\n"
                "• Budget-Friendly 💰: Economy options, cost-saving focus\n"
                "• Moderate 💵: Good value with comfort\n"
                "• Luxury 💎: Premium experiences"
            ),
            'interests': (
                "What types of activities interest you most? 🎯\n"
                "For example: culture, adventure, food, relaxation, nightlife, shopping"
            ),
            'accommodation_type': (
                "What type of accommodation do you prefer? 🏨\n"
                "• Hotels\n"
                "• Hostels (budget-friendly)\n"
                "• Vacation rentals (Airbnb/Vrbo)\n"
                "• Resorts"
            ),
            'local_transport': (
                "How would you prefer to get around at your destination? 🚇\n"
                "• Public Transportation (buses, trains, metro)\n"
                "• Rental Car\n"
                "• Ride-sharing/Taxis\n"
                "• Walking\n"
                "• Mix of options"
            )
        }
        
        return questions.get(field, f"Could you please provide information about {field}?")
    
    def ask_clarifying_question(self, context: Dict[str, Any]) -> str:
        """
        Ask a clarifying question based on current context
        
        Args:
            context: Current conversation context
            
        Returns:
            str: Clarifying question
        """
        required = self.get_required_information()
        missing = self.check_missing_information(context, required)
        
        if missing:
            return self.ask_for_information(missing[0])
        
        return "I'd love to help! Could you tell me more about what you're looking for?"
    
    def format_recommendations(self, recommendations: Dict[str, Any]) -> str:
        """
        Format travel recommendations for display
        
        Args:
            recommendations: Dictionary of recommendations
            
        Returns:
            str: Formatted recommendations
        """
        output = ["Based on your preferences, here are my recommendations:\n"]
        
        if 'destinations' in recommendations:
            output.append("🌍 **Destinations:**")
            for dest in recommendations['destinations']:
                output.append(f"  • {dest}")
            output.append("")
        
        if 'activities' in recommendations:
            output.append("🎯 **Activities:**")
            for activity in recommendations['activities']:
                output.append(f"  • {activity}")
            output.append("")
        
        if 'accommodations' in recommendations:
            output.append("🏨 **Accommodation Options:**")
            for acc in recommendations['accommodations']:
                output.append(f"  • {acc}")
            output.append("")
        
        return "\n".join(output)
    
    def format_itinerary(self, itinerary: Dict[str, Any]) -> str:
        """
        Format itinerary for display
        
        Args:
            itinerary: Dictionary containing itinerary details
            
        Returns:
            str: Formatted itinerary
        """
        output = [f"# {itinerary['title']}\n"]
        
        for day_num, day_plan in enumerate(itinerary.get('days', []), 1):
            output.append(f"\n## Day {day_num} - {day_plan.get('title', '')}")
            output.append(day_plan.get('description', ''))
            
            if 'activities' in day_plan:
                for activity in day_plan['activities']:
                    time = activity.get('time', '')
                    name = activity.get('name', '')
                    details = activity.get('details', '')
                    cost = activity.get('cost', '')
                    
                    output.append(f"\n**{time}** - {name}")
                    if details:
                        output.append(f"  {details}")
                    if cost:
                        output.append(f"  💰 {cost}")
            
            if 'daily_total' in day_plan:
                output.append(f"\n*Estimated daily spend: {day_plan['daily_total']}*")
        
        return "\n".join(output)
    
    def format_budget_breakdown(
        self, 
        breakdown: Dict[str, Any], 
        user_budget: Optional[float] = None
    ) -> str:
        """
        Format budget breakdown for display
        
        Args:
            breakdown: Budget breakdown dictionary
            user_budget: User's stated budget (optional)
            
        Returns:
            str: Formatted budget breakdown
        """
        output = ["\n# 💰 TRIP COST BREAKDOWN\n"]
        
        currency = breakdown.get('currency', '$')
        
        # Individual categories
        categories = {
            'flights': '✈️  Flights',
            'accommodation': '🏨 Accommodation',
            'local_transport': '🚇 Local Transportation',
            'meals': '🍽️  Meals',
            'activities': '🎭 Activities & Attractions',
            'miscellaneous': '💼 Miscellaneous'
        }
        
        for key, label in categories.items():
            if key in breakdown:
                output.append(f"{label}: {currency}{breakdown[key]:,.2f}")
        
        # Total
        output.append("━" * 40)
        total = breakdown.get('total', 0)
        output.append(f"**TOTAL ESTIMATED COST: {currency}{total:,.2f}**")
        
        # Budget comparison
        if user_budget:
            output.append(f"Your Budget: {currency}{user_budget:,.2f}")
            difference = user_budget - total
            if difference >= 0:
                output.append(f"✅ Under budget by: {currency}{difference:,.2f}")
            else:
                output.append(f"⚠️  Over budget by: {currency}{abs(difference):,.2f}")
        
        return "\n".join(output)
    
    def format_travel_support(self, support_info: Dict[str, Any]) -> str:
        """
        Format travel support information
        
        Args:
            support_info: Travel support information
            
        Returns:
            str: Formatted support information
        """
        output = ["# 🛂 Travel Support Information\n"]
        
        if 'visa_requirements' in support_info:
            output.append("## Visa Requirements")
            output.append(support_info['visa_requirements'])
            output.append("")
        
        if 'safety_tips' in support_info:
            output.append("## Safety Tips")
            for tip in support_info['safety_tips']:
                output.append(f"  • {tip}")
            output.append("")
        
        if 'emergency_contacts' in support_info:
            output.append("## Emergency Contacts")
            output.append(support_info['emergency_contacts'])
            output.append("")
        
        return "\n".join(output)
    
    def provide_booking_guidance(self, context: Dict[str, Any]) -> str:
        """
        Provide booking guidance to the user
        
        Args:
            context: Current conversation context
            
        Returns:
            str: Booking guidance message
        """
        return (
            "I can help guide you through the booking process! 📝\n\n"
            "Here's what I recommend:\n\n"
            "**For Flights:**\n"
            "  • Compare prices on: Skyscanner, Google Flights, Kayak\n"
            "  • Book directly with airlines when possible\n\n"
            "**For Accommodation:**\n"
            "  • Hotels: Booking.com, Hotels.com, official hotel websites\n"
            "  • Vacation rentals: Airbnb, Vrbo\n\n"
            "**For Activities:**\n"
            "  • GetYourGuide, Viator, local tour operators\n\n"
            "I can provide specific recommendations and links based on your itinerary. "
            "Would you like me to suggest specific options?"
        )
    
    def reset(self):
        """Reset conversation state"""
        self.conversation_history = []
        self.current_phase = "greeting"

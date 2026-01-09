"""
Main Travel Agent class
Coordinates all travel planning, booking assistance, and user interactions
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
from .conversation_handler import ConversationHandler
from services.travel_planner import TravelPlanner
from services.itinerary_manager import ItineraryManager
from services.budget_calculator import BudgetCalculator
from services.ai_service import AIService


class TravelAgent:
    """
    Intelligent travel agent powered by the Strands framework.
    Handles travel planning, booking assistance, and itinerary management.
    """
    def __init__(self):
        """Initialize the travel agent with necessary components"""
        self.conversation_handler = ConversationHandler()
        self.travel_planner = TravelPlanner()
        self.itinerary_manager = ItineraryManager()
        self.budget_calculator = BudgetCalculator()
        self.ai_service = AIService()
        self.user_context: Dict[str, Any] = {}
        self.ai_enabled = self.ai_service.enabled
        
    def start_conversation(self) -> str:
        """
        Start a new conversation with the user
        
        Returns:
            str: Greeting message
        """
        return self.conversation_handler.greet_user()
    
    def test_ai_connection(self) -> bool:
        """
        Test Azure OpenAI connection
        
        Returns:
            bool: True if connection successful
        """
        return self.ai_service.test_connection()
    
    def process_message(self, user_message: str) -> str:
        """
        Process user message and generate appropriate response
        
        Args:
            user_message: The user's input message
            
        Returns:
            str: Agent's response
        """
        # Use AI service if enabled for more natural responses
        if self.ai_enabled:
            return self._process_with_ai(user_message)
        
        # Fallback to rule-based processing
        return self._process_rule_based(user_message)
    
    def _process_with_ai(self, user_message: str) -> str:
        """
        Process message using AI service
        
        Args:
            user_message: User's message
            
        Returns:
            str: AI-generated response
        """
        # Update user context
        self.user_context = self.conversation_handler.extract_context(
            user_message, 
            self.user_context
        )
        
        # Get AI response with context
        return self.ai_service.get_ai_response(user_message, self.user_context)
    
    def _process_rule_based(self, user_message: str) -> str:
        """
        Process message using rule-based logic
        
        Args:
            user_message: User's message
            
        Returns:
            str: Rule-based response
        """
        # Parse user intent
        intent = self.conversation_handler.parse_intent(user_message)
        
        # Update user context
        self.user_context = self.conversation_handler.extract_context(
            user_message, 
            self.user_context
        )
        
        # Handle based on intent
        if intent == "plan_trip":
            return self._handle_trip_planning()
        elif intent == "get_recommendations":
            return self._handle_recommendations()
        elif intent == "create_itinerary":
            return self._handle_itinerary_creation()
        elif intent == "calculate_budget":
            return self._handle_budget_calculation()
        elif intent == "booking_assistance":
            return self._handle_booking_assistance()
        elif intent == "travel_support":
            return self._handle_travel_support()
        else:
            return self.conversation_handler.ask_clarifying_question(self.user_context)
    
    def _handle_trip_planning(self) -> str:
        """Handle trip planning requests"""
        # Check if we have enough information
        required_info = self.conversation_handler.get_required_information()
        missing_info = self.conversation_handler.check_missing_information(
            self.user_context, 
            required_info
        )
        
        if missing_info:
            return self.conversation_handler.ask_for_information(missing_info[0])
        
        # Generate travel recommendations
        recommendations = self.travel_planner.generate_recommendations(
            self.user_context
        )
        
        return self.conversation_handler.format_recommendations(recommendations)
    
    def _handle_recommendations(self) -> str:
        """Handle recommendation requests"""
        if not self.user_context.get('destination'):
            return "I'd love to help you with recommendations! Where are you planning to travel?"
        
        recommendations = self.travel_planner.get_destination_recommendations(
            destination=self.user_context.get('destination'),
            interests=self.user_context.get('interests', []),
            budget=self.user_context.get('budget')
        )
        
        return self.conversation_handler.format_recommendations(recommendations)
    
    def _handle_itinerary_creation(self) -> str:
        """Handle itinerary creation requests"""
        if not self._has_minimum_trip_info():
            return self.conversation_handler.ask_clarifying_question(self.user_context)
        
        # Create detailed itinerary
        itinerary = self.itinerary_manager.create_itinerary(
            destination=self.user_context['destination'],
            duration=self.user_context['duration'],
            interests=self.user_context.get('interests', []),
            budget=self.user_context.get('budget'),
            accommodation_pref=self.user_context.get('accommodation_type'),
            transport_pref=self.user_context.get('local_transport')
        )
        
        return self.conversation_handler.format_itinerary(itinerary)
    
    def _handle_budget_calculation(self) -> str:
        """Handle budget calculation requests"""
        if not self._has_minimum_trip_info():
            return "To calculate your trip budget, I need some basic information. " + \
                   self.conversation_handler.ask_clarifying_question(self.user_context)
        
        # Calculate comprehensive budget
        budget_breakdown = self.budget_calculator.calculate_total_cost(
            origin=self.user_context.get('origin'),
            destination=self.user_context.get('destination'),
            duration=self.user_context.get('duration'),
            budget_level=self.user_context.get('budget_level', 'moderate'),
            accommodation_type=self.user_context.get('accommodation_type'),
            activities=self.user_context.get('planned_activities', [])
        )
        
        return self.conversation_handler.format_budget_breakdown(
            budget_breakdown,
            self.user_context.get('budget')
        )
    
    def _handle_booking_assistance(self) -> str:
        """Handle booking assistance requests"""
        return self.conversation_handler.provide_booking_guidance(self.user_context)
    
    def _handle_travel_support(self) -> str:
        """Handle travel support and guidance requests"""
        destination = self.user_context.get('destination')
        if not destination:
            return "I can help with travel support! Which destination do you need information about?"
        
        support_info = self.travel_planner.get_travel_support_info(destination)
        return self.conversation_handler.format_travel_support(support_info)
    
    def _has_minimum_trip_info(self) -> bool:
        """
        Check if we have minimum required information for trip planning
        
        Returns:
            bool: True if minimum info is available
        """
        return (
            'destination' in self.user_context and 
            'duration' in self.user_context
        )
    
    def reset_conversation(self):
        """Reset conversation and user context"""
        self.user_context = {}
        self.conversation_handler.reset()
        self.ai_service.reset_conversation()

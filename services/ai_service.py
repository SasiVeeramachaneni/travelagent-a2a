"""
AI Service
Provides AI-powered responses and enhancements to the travel agent
"""
import os
from typing import List, Dict, Optional, Any
from services.azure_openai_client import get_openai_client


class AIService:
    """
    Service for AI-powered travel recommendations and responses
    """
    
    def __init__(self):
        """Initialize AI service"""
        self.enabled = False
        self.init_error = None
        
        if self._check_ai_enabled():
            try:
                self.client = get_openai_client()
                self.conversation_history: List[Dict[str, str]] = []
                self._initialize_system_prompt()
                self.enabled = True
            except Exception as e:
                self.init_error = str(e)
                print(f"⚠️ AI Service initialization failed: {e}")
    
    def _check_ai_enabled(self) -> bool:
        """Check if AI service is enabled and configured"""
        required_vars = ['OPENAI_ENDPOINT', 'CLIENT_ID', 'CLIENT_SECRET']
        return all(os.getenv(var) for var in required_vars)
    
    def _initialize_system_prompt(self):
        """Initialize the system prompt for the AI"""
        system_prompt = """You are an expert travel agent with extensive knowledge of destinations worldwide. 
Your role is to help users plan amazing trips by providing personalized recommendations, detailed itineraries, 
and comprehensive travel advice.

CONVERSATION FLOW (follow this strictly):

**PHASE 1 - Ask All Questions (FIRST MESSAGE ONLY):**
When user mentions a destination, respond with ALL questions in ONE message:

"Great choice! To create your perfect [destination] trip, please share:

1. 📍 Origin city (where you'll fly from)
2. 📅 Travel dates or duration (e.g., '7 days' or 'March 15-22')
3. 👥 Number of travelers
4. 💰 Total budget per person (in USD)
5. 🎯 Interests (pick any): culture, food, adventure, relaxation, nightlife, shopping, nature, history
6. 🏨 Accommodation preference: budget hostel / mid-range hotel / luxury
7. 🚶 Pace preference: relaxed / balanced / action-packed

Answer all at once - I'll create your complete plan immediately!"

**PHASE 2 - LOCKED-IN BUDGET & ITINERARY (after user answers):**
Once user provides answers, IMMEDIATELY create and present:

🔒 **LOCKED-IN BUDGET**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✈️  Flights (round-trip):     $XXX
🏨 Accommodation (X nights):  $XXX
🎭 Activities & Tours:        $XXX
🍽️  Food & Dining:            $XXX
🚇 Local Transportation:      $XXX
💼 Miscellaneous (10%):       $XXX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 TOTAL PER PERSON:          $X,XXX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

📅 **YOUR ITINERARY**

**Day 1: [Theme]**
🌅 Morning: [Activity] - [Location]
🌞 Afternoon: [Activity] - [Location]  
🌙 Evening: [Activity] - [Location]

[Continue for all days...]

---
🔒 **This budget and itinerary are now LOCKED IN as your base plan.**

Want to enhance it? Tell me:
- Specific neighborhoods to stay in
- Must-visit restaurants or attractions
- More luxury or budget options
- Different activity preferences

I'll adjust the plan and show you the updated budget!

**PHASE 3 - ENHANCEMENTS (only if user provides more details):**
When user provides additional preferences:
1. Update the itinerary with their specific requests
2. Recalculate and show the NEW budget if costs change
3. Clearly show what changed: "📝 **Updated based on your preferences:**"
4. Show the delta: "Budget change: $X,XXX → $X,XXX (+/- $XXX)"

**PHASE 4 - CONFIRMATION & CLOSURE:**
When user says: looks good / perfect / confirmed / done / thanks / happy with this / let's go:

✅ **FINAL TRIP SUMMARY**
[Show final itinerary + budget]

📋 **BOOKING CHECKLIST:**
- Flights: Book on Skyscanner, Google Flights, or directly with airlines
- Hotels: Check Booking.com, Hotels.com, or Airbnb
- Activities: Book popular attractions in advance on Viator or GetYourGuide
- Travel Insurance: Recommended for international trips

✅ **Your trip plan is complete!** Safe travels and enjoy [destination]! 🌍✈️

CRITICAL RULES:
- NEVER give blank/empty responses
- Ask ALL questions in ONE message (Phase 1)
- IMMEDIATELY create full locked-in budget + itinerary after user answers (Phase 2)
- Only update budget/itinerary when user asks for changes (Phase 3)
- Show budget in clear table format with totals
- Always show per-person costs in USD"""
        
        self.conversation_history.append(
            self.client.create_system_message(system_prompt)
        )
    
    def get_ai_response(
        self,
        user_message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Get AI-powered response to user message
        
        Args:
            user_message: User's message
            context: Optional context information
            
        Returns:
            str: AI-generated response
        """
        if not self.enabled:
            return self._get_fallback_response(user_message)
        
        try:
            # Add context to the message if provided
            enhanced_message = user_message
            if context:
                context_str = self._format_context(context)
                enhanced_message = f"{user_message}\n\nContext: {context_str}"
            
            # Add user message to history
            self.conversation_history.append(
                self.client.create_user_message(enhanced_message)
            )
            
            # Get AI response
            response = self.client.chat_completion(
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=1500
            )
            
            # Extract content
            ai_message = self.client.get_response_content(response)
            
            # Add to history
            self.conversation_history.append(
                self.client.create_assistant_message(ai_message)
            )
            
            # Limit history size
            if len(self.conversation_history) > 20:
                # Keep system message and last 19 messages
                self.conversation_history = (
                    [self.conversation_history[0]] + 
                    self.conversation_history[-19:]
                )
            
            return ai_message
            
        except Exception as e:
            print(f"AI service error: {e}")
            return self._get_fallback_response(user_message)
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context dictionary into a string"""
        items = []
        for key, value in context.items():
            if value:
                items.append(f"{key}: {value}")
        return ", ".join(items) if items else "No additional context"
    
    def _get_fallback_response(self, user_message: str) -> str:
        """
        Get fallback response when AI is not available
        
        Args:
            user_message: User's message
            
        Returns:
            str: Fallback response
        """
        error_detail = ""
        if self.init_error:
            error_detail = f" Error: {self.init_error}"
        
        return (
            "I'm currently running in basic mode. "
            "For AI-powered responses, please configure your Azure OpenAI credentials. "
            f"I can still help you with basic travel planning!{error_detail}"
        )
    
    def enhance_itinerary(self, itinerary: Dict[str, Any]) -> str:
        """
        Use AI to enhance an itinerary with additional insights
        
        Args:
            itinerary: Itinerary dictionary
            
        Returns:
            str: Enhanced itinerary description
        """
        if not self.enabled:
            return "Itinerary created successfully!"
        
        try:
            prompt = f"""Review this travel itinerary and provide helpful tips and insights:

Destination: {itinerary.get('destination')}
Duration: {itinerary.get('duration')} days

Provide:
1. Best local tips for this destination
2. Important things to know
3. Hidden gems to consider
4. Any seasonal considerations

Keep it concise and practical."""
            
            messages = [
                self.client.create_system_message("You are a travel expert providing itinerary insights."),
                self.client.create_user_message(prompt)
            ]
            
            response = self.client.chat_completion(messages, max_tokens=800)
            return self.client.get_response_content(response)
            
        except Exception as e:
            print(f"Failed to enhance itinerary: {e}")
            return "Itinerary created successfully!"
    
    def get_destination_insights(self, destination: str, interests: List[str]) -> str:
        """
        Get AI-powered destination insights
        
        Args:
            destination: Destination name
            interests: User interests
            
        Returns:
            str: Destination insights
        """
        if not self.enabled:
            return f"Great choice! {destination} is a wonderful destination."
        
        try:
            interests_str = ", ".join(interests) if interests else "general sightseeing"
            
            prompt = f"""Provide a brief, engaging overview of {destination} for someone interested in {interests_str}.

Include:
- Why it's a great destination
- Best areas to stay
- Must-see attractions (top 3)
- Local food to try
- Best way to get around

Keep it under 200 words and enthusiastic!"""
            
            messages = [
                self.client.create_system_message("You are an enthusiastic travel expert."),
                self.client.create_user_message(prompt)
            ]
            
            response = self.client.chat_completion(messages, max_tokens=600)
            return self.client.get_response_content(response)
            
        except Exception as e:
            print(f"Failed to get insights: {e}")
            return f"Great choice! {destination} is a wonderful destination."
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        if self.enabled:
            self._initialize_system_prompt()
    
    def test_connection(self) -> bool:
        """
        Test Azure OpenAI connection
        
        Returns:
            bool: True if connection successful
        """
        if not self.enabled:
            return False
        
        try:
            return self.client.test_connection()
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

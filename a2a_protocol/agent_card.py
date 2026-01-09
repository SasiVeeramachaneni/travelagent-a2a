"""
Agent Card Definition for Travel Agent
Defines the agent's capabilities, skills, and metadata for A2A discovery
"""
from a2a.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill,
    OAuth2SecurityScheme,
    OAuthFlows,
    ClientCredentialsOAuthFlow,
)
from typing import Optional


def create_agent_card(
    host: str = "localhost",
    port: int = 8000,
    version: str = "1.0.0",
    include_oauth2: bool = True
) -> AgentCard:
    """
    Create the Agent Card for the Travel Agent
    
    The Agent Card is the discovery document that other agents use to understand
    this agent's capabilities, skills, and how to interact with it.
    
    Args:
        host: The hostname where the agent is running
        port: The port number
        version: Agent version
        include_oauth2: Whether to include OAuth2 security scheme
        
    Returns:
        AgentCard: The complete agent card for A2A discovery
    """
    
    # Determine the base URL
    if host in ("localhost", "127.0.0.1"):
        base_url = f"http://{host}:{port}"
    else:
        base_url = f"https://{host}"
    
    # Define the agent's skills
    skills = [
        AgentSkill(
            id="plan_trip",
            name="Plan Trip",
            description="Plan a complete trip including destination recommendations, "
                       "accommodations, activities, and budget estimation. Provide "
                       "destination, dates, budget, and preferences for best results.",
            tags=["travel", "planning", "trip", "vacation"],
            examples=[
                "Plan a 7-day trip to Tokyo with a budget of $3000",
                "Help me plan a romantic getaway to Paris in spring",
                "I want to visit Bali for 10 days, budget-friendly options please"
            ]
        ),
        AgentSkill(
            id="get_recommendations",
            name="Get Travel Recommendations",
            description="Get personalized travel recommendations for destinations, "
                       "hotels, restaurants, and activities based on preferences "
                       "and interests.",
            tags=["recommendations", "destinations", "hotels", "activities"],
            examples=[
                "What are the best beaches to visit in Thailand?",
                "Recommend family-friendly activities in Orlando",
                "Suggest romantic restaurants in Rome"
            ]
        ),
        AgentSkill(
            id="calculate_budget",
            name="Calculate Trip Budget",
            description="Calculate a comprehensive travel budget including flights, "
                       "accommodations, meals, activities, and transportation costs.",
            tags=["budget", "cost", "finance", "estimation"],
            examples=[
                "How much will a week in London cost?",
                "Calculate budget for 2 people visiting Japan for 14 days",
                "What's a realistic budget for backpacking through Europe?"
            ]
        ),
        AgentSkill(
            id="create_itinerary",
            name="Create Detailed Itinerary",
            description="Create a day-by-day travel itinerary with activities, "
                       "timings, and logistics for your trip.",
            tags=["itinerary", "schedule", "planning", "daily"],
            examples=[
                "Create a 5-day itinerary for New York City",
                "Plan my daily schedule for a week in Barcelona",
                "Make an itinerary for a road trip from LA to San Francisco"
            ]
        ),
        AgentSkill(
            id="travel_info",
            name="Travel Information",
            description="Provide essential travel information including visa "
                       "requirements, weather, cultural tips, safety information, "
                       "and local customs for destinations.",
            tags=["visa", "weather", "culture", "safety", "information"],
            examples=[
                "Do I need a visa to visit Vietnam from USA?",
                "What's the best time to visit Iceland?",
                "Tell me about local customs in Japan"
            ]
        ),
        AgentSkill(
            id="booking_assistance",
            name="Booking Assistance",
            description="Provide guidance and assistance with booking flights, "
                       "hotels, and activities including tips for finding deals.",
            tags=["booking", "flights", "hotels", "deals"],
            examples=[
                "Help me find cheap flights to Hawaii",
                "Where should I book hotels in Amsterdam?",
                "Tips for booking activities in advance"
            ]
        )
    ]
    
    # Define agent capabilities
    capabilities = AgentCapabilities(
        streaming=False,  # We'll start with non-streaming responses
        push_notifications=False,
        state_transition_history=False
    )
    
    # Define OAuth2 security scheme if enabled
    security_schemes = None
    security = None
    
    if include_oauth2:
        # OAuth2 Client Credentials Flow
        security_schemes = {
            "oauth2": OAuth2SecurityScheme(
                type="oauth2",
                description="OAuth2 Client Credentials authentication for agent-to-agent communication",
                flows=OAuthFlows(
                    client_credentials=ClientCredentialsOAuthFlow(
                        token_url="/oauth/token",
                        scopes={
                            "a2a:travel-agent": "Access to Travel Agent A2A endpoints"
                        }
                    )
                )
            )
        }
        # Require oauth2 security for all operations
        security = [{"oauth2": ["a2a:travel-agent"]}]
    
    # Create and return the agent card
    return AgentCard(
        name="Travel Agent",
        description="An intelligent AI-powered travel agent that helps with trip "
                   "planning, destination recommendations, budget calculation, "
                   "itinerary creation, and travel information. Powered by Azure "
                   "OpenAI for natural, conversational interactions. "
                   "Requires OAuth2 authentication (client_credentials flow).",
        url=base_url,
        version=version,
        capabilities=capabilities,
        skills=skills,
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        security_schemes=security_schemes,
        security=security,
    )

"""
Travel Agent - Main Entry Point
An intelligent travel agent powered by the Strands framework
"""
import os
from dotenv import load_dotenv
from agent.travel_agent import TravelAgent
from config import get_config, Config


def load_environment():
    """Load environment variables from .env file"""
    # Load .env file
    load_dotenv()
    
    # Check if required variables are set
    required_vars = ['OPENAI_ENDPOINT', 'CLIENT_ID', 'CLIENT_SECRET']
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print("⚠️  Warning: Some Azure OpenAI credentials are not configured.")
        print(f"   Missing: {', '.join(missing)}")
        print("   The agent will run in basic mode without AI enhancements.")
        print("   Please configure your .env file for full functionality.\n")
        return False
    
    return True


def test_ai_connection(agent: TravelAgent) -> bool:
    """Test Azure OpenAI connection"""
    print("Testing Azure OpenAI connection...", end=" ")
    try:
        if agent.test_ai_connection():
            print("✅ Connected successfully!")
            return True
        else:
            print("❌ Connection failed")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main function to run the travel agent"""
    # Load environment variables
    ai_configured = load_environment()
    
    # Load configuration
    config = get_config('development')
    
    # Initialize the travel agent
    agent = TravelAgent()
    
    # Start conversation
    print("=" * 60)
    print(f"  {Config.APP_NAME} v{Config.APP_VERSION}")
    print("=" * 60)
    
    # Show AI status
    if agent.ai_enabled:
        print("🤖 AI Mode: ENABLED (Azure OpenAI)")
        if ai_configured:
            test_ai_connection(agent)
    else:
        print("🤖 AI Mode: DISABLED (Basic rule-based responses)")
    
    print("=" * 60)
    print()
    
    # Greet the user
    greeting = agent.start_conversation()
    print(greeting)
    print()
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("\nThank you for using Travel Agent! Have a wonderful trip! ✈️ 🌍")
                break
            
            # Check for reset command
            if user_input.lower() in ['reset', 'restart', 'new']:
                agent.reset_conversation()
                print("\nConversation reset. Let's start fresh!")
                greeting = agent.start_conversation()
                print(greeting)
                print()
                continue
            
            # Check for test connection command
            if user_input.lower() in ['test', 'test connection']:
                test_ai_connection(agent)
                continue
            
            # Skip empty input
            if not user_input:
                continue
            
            # Process the message
            response = agent.process_message(user_input)
            print(f"\nAgent: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Safe travels! ✈️")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again or type 'exit' to quit.\n")


def demo_mode():
    """Run a demo of the travel agent with sample interactions"""
    agent = TravelAgent()
    
    print("=" * 60)
    print("  TRAVEL AGENT DEMO MODE")
    print("=" * 60)
    print()
    
    # Sample conversation flow
    demo_messages = [
        "I want to plan a trip to Paris",
        "I'm traveling from New York",
        "I have 5 days",
        "My budget is around $3000",
        "I'm interested in culture, food, and some sightseeing",
        "I prefer to use public transportation",
        "Can you create an itinerary for me?",
        "What will be the total cost?"
    ]
    
    # Start
    print(agent.start_conversation())
    print()
    
    for message in demo_messages:
        print(f"User: {message}")
        response = agent.process_message(message)
        print(f"\nAgent: {response}\n")
        print("-" * 60)
        input("Press Enter to continue...")
        print()


if __name__ == '__main__':
    import sys
    
    # Check for demo mode
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo_mode()
    else:
        main()

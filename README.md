# Travel Agent Project

An intelligent travel agent powered by Azure OpenAI and the Strands framework. This application assists users with all aspects of travel planning, booking, and support using AI-powered natural language conversations.

## Features

- **🤖 AI-Powered Conversations**: Natural language interaction using Azure OpenAI
- **✈️ Travel Planning & Research**: Personalized destination recommendations
- **💰 Budget Management**: Detailed cost breakdowns and budget optimization
- **📅 Itinerary Creation**: Day-by-day travel itineraries with timings and activities
- **🔐 Azure AD Authentication**: Secure authentication using client credentials
- **🌍 Multi-destination Support**: Pre-configured data for popular destinations

## Project Structure

```
travelagent/
├── agent/                      # Core agent module
│   ├── __init__.py
│   ├── travel_agent.py        # Main TravelAgent class
│   └── conversation_handler.py # Conversation management
├── services/                   # Business logic services
│   ├── __init__.py
│   ├── travel_planner.py      # Travel planning service
│   ├── itinerary_manager.py   # Itinerary creation and management
│   └── budget_calculator.py   # Budget calculation service
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── models.py              # Data models
│   └── helpers.py             # Helper functions
├── knowledge/                  # Knowledge base (empty - for future use)
├── config.py                   # Configuration settings
├── main.py                     # Main entry point
├── AGENT_INSTRUCTIONS.md       # Detailed agent instructions
└── README.md                   # This file
```
## Installation

### Prerequisites
- Python 3.8 or higher
- Azure OpenAI account with deployment
- Azure AD App Registration with client credentials

### Step 1: Clone or Download the Project

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `requests` - For Azure OpenAI API calls
## Usage

### Quick Start

```bash
python main.py
```

### First Time Setup

When you run the agent for the first time:

1. The agent will show connection status:
```
============================================================
  Travel Agent v1.0.0
============================================================
🤖 AI Mode: ENABLED (Azure OpenAI)
Testing Azure OpenAI connection... ✅ Connected successfully!
============================================================
```

2. Start chatting naturally with the agent:
```
Agent: Hello! 👋 I'm your intelligent travel agent...

You: I want to plan a trip to Paris
Agent: That's wonderful! Paris is an amazing destination...
```

### Available Commands

During conversation:
- `exit`, `quit`, `bye`, `goodbye` - Exit the application
- `reset`, `restart`, `new` - Start a new conversation
- `test`, `test connection` - Test Azure OpenAI connection

### AI vs Basic Mode

**AI Mode (Recommended)**:
- Natural language understanding
- Context-aware responses
- Personalized recommendations
- Requires Azure OpenAI credentials

**Basic Mode**:
- Rule-based responses
- Works without AI credentials
- Limited conversation understanding
- Good for testing basic functionality

### Azure OpenAI Endpoint
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource
3. Copy the endpoint URL from the "Keys and Endpoint" section

### Azure AD App Registration
1. Go to Azure Portal → Azure Active Directory → App Registrations
2. Create a new registration or use existing
3. Get your credentials:
   - **Tenant ID**: From app Overview page
   - **Client ID**: From app Overview page (Application ID)
   - **Client Secret**: Certificates & secrets → New client secret

### Assign Permissions
1. Go to your Azure OpenAI resource
2. Access Control (IAM) → Add role assignment
3. Assign "Cognitive Services User" role to your App Registrationo external dependencies required yet
```

## Usage

### Interactive Mode

Run the travel agent in interactive mode:

```bash
python main.py
```

This starts a conversation with the agent where you can:
- Plan trips
- Get destination recommendations
- Create detailed itineraries
- Calculate trip budgets
- Get travel support information

Example conversation:
```
You: I want to plan a trip to Paris
Agent: That's wonderful! Paris is an amazing destination...

You: I have 5 days and a budget of $3000
Agent: Perfect! Let me help you plan...

You: Create an itinerary for me
Agent: Here's your detailed 5-day Paris itinerary...
```

### Demo Mode

Run a pre-configured demo:

```bash
python main.py --demo
```

### Available Commands

During conversation:
- `exit`, `quit`, `bye`, `goodbye` - Exit the application
- `reset`, `restart`, `new` - Start a new conversation

## Key Components

### TravelAgent
The main agent class that coordinates all travel planning activities.

### ConversationHandler
Manages user interactions, intent parsing, and response formatting.

### TravelPlanner
Provides destination research, recommendations, and travel planning logic.

### ItineraryManager
Creates and manages detailed day-by-day travel itineraries.

### BudgetCalculator
Calculates comprehensive trip costs with detailed breakdowns including:
- Flights
- Accommodation
- Meals
- Local transportation
- Activities
- Miscellaneous (15% buffer)

## Configuration

Edit `config.py` to modify:
- Default budget levels
- Supported destinations
- Currency settings
- Feature flags
- API keys (for future integrations)

## Supported Destinations

Currently pre-configured with data for:
- Paris, France
- Tokyo, Japan
- New York, USA

Generic recommendations available for other destinations.

## Future Enhancements

- [ ] Real-time flight and hotel API integration
- [ ] Weather data integration
- [ ] Actual booking capabilities
- [ ] Multi-language support
- [ ] Mobile app interface
- [ ] User authentication and trip history
- [ ] Collaborative trip planning
- [ ] Integration with mapping services
- [ ] PDF itinerary export
- [ ] Email notifications and confirmations

## Development

### Adding New Destinations

To add a new destination, update the `_load_destination_data()` method in `services/travel_planner.py` and `_load_pricing_data()` in `services/budget_calculator.py`.

### Running Tests

(Tests to be implemented)
```bash
python -m pytest tests/
```

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational and demonstration purposes.

## Contact

For questions or support, please refer to the project documentation.

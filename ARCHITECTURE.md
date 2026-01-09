# Travel Agent - System Architecture

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                          (main.py)                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TRAVEL AGENT                               │
│                  (agent/travel_agent.py)                        │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │ AI Enabled?  │───>│ AI Mode      │    │ Basic Mode   │    │
│  └──────────────┘    └──────┬───────┘    └──────┬───────┘    │
└─────────────────────────────┼────────────────────┼─────────────┘
                              │                    │
                              ▼                    ▼
        ┌─────────────────────────────┐   ┌─────────────────────┐
        │      AI SERVICE             │   │ CONVERSATION        │
        │  (services/ai_service.py)   │   │ HANDLER             │
        └───────────┬─────────────────┘   └─────────────────────┘
                    │
                    ▼
        ┌─────────────────────────────┐
        │  AZURE OPENAI CLIENT        │
        │  (azure_openai_client.py)   │
        └───────────┬─────────────────┘
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│  AZURE AD        │  │  AZURE OPENAI    │
│  Authentication  │  │  API             │
└──────────────────┘  └──────────────────┘
```

## Authentication Flow

```
┌──────────────┐
│ Application  │
│   Starts     │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────┐
│ Load .env Credentials        │
│ - TENANT_ID                  │
│ - CLIENT_ID                  │
│ - CLIENT_SECRET              │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ AzureOpenAIClient.__init__() │
│ - Validate config            │
│ - Initialize token vars      │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ First API Call Needed        │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ _get_access_token()          │
│ - Check if token cached      │
│ - Check if token valid       │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Request Token from Azure AD  │
│ POST to TOKEN_URL            │
│ - grant_type: client_creds   │
│ - client_id                  │
│ - client_secret              │
│ - scope: cognition services  │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Receive Access Token         │
│ - Cache token                │
│ - Set expiry time            │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Make API Call                │
│ - Add Bearer token to header │
│ - POST to OpenAI endpoint    │
│ - Send messages payload      │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Receive & Parse Response     │
│ - Extract content            │
│ - Return to application      │
└──────────────────────────────┘
```

## Data Flow

```
User Message
    │
    ▼
┌─────────────────────┐
│ Input Sanitization  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Context Extraction  │
│ - Parse budget      │
│ - Parse duration    │
│ - Parse interests   │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ AI Service Check    │
└─────────┬───────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌───────┐   ┌──────────┐
│  AI   │   │  Basic   │
│ Mode  │   │  Mode    │
└───┬───┘   └────┬─────┘
    │            │
    ▼            ▼
┌─────────┐  ┌──────────┐
│ OpenAI  │  │ Rule     │
│ API     │  │ Based    │
└───┬─────┘  └────┬─────┘
    │            │
    └────┬───────┘
         ▼
┌─────────────────────┐
│ Format Response     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Display to User     │
└─────────────────────┘
```

## Service Dependencies

```
TravelAgent
    ├── ConversationHandler (always)
    ├── TravelPlanner (always)
    ├── ItineraryManager (always)
    ├── BudgetCalculator (always)
    └── AIService (conditional)
            └── AzureOpenAIClient (conditional)
                    ├── requests library
                    └── Azure AD + Azure OpenAI
```

## Configuration Loading

```
Application Start
    │
    ▼
┌──────────────────────┐
│ Load .env file       │
│ (python-dotenv)      │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Config class loads   │
│ environment vars     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Services initialize  │
│ using Config values  │
└──────────────────────┘
```

## Mode Selection Logic

```
┌──────────────────────┐
│ Check Credentials    │
│ - OPENAI_ENDPOINT    │
│ - CLIENT_ID          │
│ - CLIENT_SECRET      │
└──────┬───────────────┘
       │
   ┌───┴───┐
   │ All   │
   │ Set?  │
   └───┬───┘
       │
   ┌───┴────────────┐
   │                │
   YES              NO
   │                │
   ▼                ▼
┌──────────┐   ┌──────────┐
│ AI Mode  │   │  Basic   │
│ Enabled  │   │   Mode   │
│          │   │          │
│ Natural  │   │  Rule    │
│ Language │   │  Based   │
└──────────┘   └──────────┘
```

## Error Handling Hierarchy

```
┌──────────────────────────────┐
│ Try AI Service               │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Authentication Error?        │
└──────┬───────────────────────┘
       │
   ┌───┴───┐
   YES     NO
   │       │
   ▼       ▼
┌─────┐  ┌──────────────────┐
│Fall │  │ API Call Error?  │
│back │  └────┬─────────────┘
│     │       │
│     │   ┌───┴───┐
│     │   YES     NO
│     │   │       │
│     ◄───┘       ▼
│                ┌──────────┐
│                │ Success  │
│                │ Return   │
│                │ Response │
└────►           └──────────┘
Basic Mode
Response
```

## Token Lifecycle

```
Token Requested
    │
    ▼
┌──────────────┐
│ Check Cache  │
└──────┬───────┘
       │
   ┌───┴────┐
   │Exists &│
   │Valid?  │
   └───┬────┘
       │
   ┌───┴─────┐
   YES       NO
   │         │
   │         ▼
   │    ┌─────────────┐
   │    │ Request New │
   │    │ from Azure  │
   │    │ AD          │
   │    └──────┬──────┘
   │           │
   │           ▼
   │    ┌─────────────┐
   │    │ Cache Token │
   │    │ Set Expiry  │
   │    └──────┬──────┘
   │           │
   └──────┬────┘
          │
          ▼
    ┌──────────┐
    │ Return   │
    │ Token    │
    └──────────┘
```

## File Organization

```
travelagent/
│
├── Configuration
│   ├── .env (credentials - gitignored)
│   ├── .env.example (template)
│   └── config.py (Config class)
│
├── Core Application
│   ├── main.py (entry point)
│   └── agent/
│       ├── travel_agent.py (main agent)
│       └── conversation_handler.py
│
├── Services
│   ├── services/
│       ├── azure_openai_client.py (NEW)
│       ├── ai_service.py (NEW)
│       ├── travel_planner.py
│       ├── itinerary_manager.py
│       └── budget_calculator.py
│
├── Utilities
│   ├── utils/
│       ├── models.py
│       └── helpers.py
│   ├── setup_check.py (NEW)
│   └── test_credentials.py (NEW)
│
└── Documentation
    ├── README.md
    ├── AGENT_INSTRUCTIONS.md
    ├── AZURE_OPENAI_GUIDE.md (NEW)
    ├── INTEGRATION_SUMMARY.md (NEW)
    └── ARCHITECTURE.md (this file - NEW)
```

## Conversation State Management

```
┌──────────────────────────────┐
│ User starts conversation     │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Initialize:                  │
│ - user_context = {}          │
│ - conversation_history = []  │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ User sends message           │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Extract context from message │
│ - Update user_context        │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Add to conversation_history  │
│ - Keep last 20 messages      │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Process with AI/Rules        │
│ - Use accumulated context    │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Generate response            │
│ - Add to history             │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Return to user               │
└──────────────────────────────┘
```

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Graceful degradation
- ✅ Secure authentication
- ✅ Scalable design
- ✅ Easy testing
- ✅ Maintainable codebase

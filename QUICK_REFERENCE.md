# Travel Agent - Quick Reference Card

## 🚀 Quick Start (3 Steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure credentials
cp .env.example .env
# Edit .env with your Azure credentials

# 3. Run
python main.py
```

## 📋 Essential Commands

| Command | Description |
|---------|-------------|
| `python main.py` | Start the travel agent |
| `python setup_check.py` | Verify complete setup |
| `python test_credentials.py` | Test Azure credentials |
| `python main.py --demo` | Run demo mode |

## 💬 In-App Commands

| Command | Action |
|---------|--------|
| `exit`, `quit`, `bye` | Exit application |
| `reset`, `restart`, `new` | Start new conversation |
| `test`, `test connection` | Test Azure connection |

## 🔑 Required Environment Variables

```bash
OPENAI_ENDPOINT=https://your-resource.openai.azure.com
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
TOKEN_URL=https://login.microsoftonline.com/common/oauth2/v2.0/token
TOKEN_SCOPE=https://cognitiveservices.azure.com/.default
OPENAI_DEPLOYMENT=gpt-4
```

## 📁 Project Structure

```
travelagent/
├── .env                         # Your credentials (DO NOT COMMIT)
├── .env.example                 # Template
├── main.py                      # Start here
├── config.py                    # Configuration
├── requirements.txt             # Dependencies
│
├── agent/                       # Core agent
│   ├── travel_agent.py         # Main agent class
│   └── conversation_handler.py # Conversation logic
│
├── services/                    # Business logic
│   ├── azure_openai_client.py  # Azure OpenAI integration
│   ├── ai_service.py           # AI service wrapper
│   ├── travel_planner.py       # Travel planning
│   ├── itinerary_manager.py    # Itinerary creation
│   └── budget_calculator.py    # Budget calculations
│
└── utils/                       # Utilities
    ├── models.py               # Data models
    └── helpers.py              # Helper functions
```

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Missing required configuration" | Update .env with actual values |
| "Failed to obtain token" | Check CLIENT_ID, CLIENT_SECRET, TENANT_ID |
| "API request failed" | Verify OPENAI_ENDPOINT and deployment name |
| "Module not found" | Run `pip install -r requirements.txt` |
| AI not working | Run `python test_credentials.py` |

## 🎯 Common Tasks

### Get Azure Credentials

1. **Azure Portal** → **Azure OpenAI**
   - Copy endpoint URL

2. **Azure AD** → **App Registrations** → **New registration**
   - Get Client ID (Application ID)
   - Create Client Secret
   - Get Tenant ID

3. **Azure OpenAI** → **Access Control (IAM)**
   - Add role: "Cognitive Services User"
   - Assign to: Your App Registration

### Test Your Setup

```bash
# Method 1: Full check
python setup_check.py

# Method 2: Credentials only
python test_credentials.py

# Method 3: In-app
python main.py
# Type: test
```

### Example Conversation

```
You: I want to plan a trip to Paris
Agent: That's wonderful! Paris is an amazing destination...

You: I have 5 days and a budget of $3000
Agent: Perfect! Let me create a plan for you...

You: Create an itinerary
Agent: Here's your detailed 5-day Paris itinerary...

You: What's the total cost?
Agent: [Detailed budget breakdown]
```

## 🔒 Security Checklist

- [ ] .env file in .gitignore
- [ ] No credentials in code
- [ ] .env.example has no real values
- [ ] CLIENT_SECRET kept secure
- [ ] Regular credential rotation

## 📊 Modes of Operation

### AI Mode (Recommended)
✅ Natural language  
✅ Context-aware  
✅ Personalized  
⚙️ Requires Azure credentials  

### Basic Mode (Fallback)
✅ Rule-based  
✅ Works without credentials  
⚠️ Limited understanding  

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | General overview and setup |
| `AZURE_OPENAI_GUIDE.md` | Detailed Azure integration |
| `INTEGRATION_SUMMARY.md` | What changed and why |
| `ARCHITECTURE.md` | System architecture diagrams |
| `AGENT_INSTRUCTIONS.md` | Agent behavior specification |
| This file | Quick reference |

## 🔗 Useful Links

- [Azure Portal](https://portal.azure.com)
- [Azure OpenAI Docs](https://learn.microsoft.com/azure/cognitive-services/openai/)
- [Azure AD App Registration](https://learn.microsoft.com/azure/active-directory/develop/quickstart-register-app)

## 💡 Pro Tips

1. **Test incrementally**: Run `setup_check.py` after each config change
2. **Monitor costs**: Check Azure portal regularly
3. **Use GPT-3.5**: For testing to reduce costs
4. **Keep history short**: Limited to 20 messages automatically
5. **Review logs**: Application shows helpful error messages

## 🆘 Getting Help

1. Run diagnostics: `python setup_check.py`
2. Check Azure portal for service status
3. Review error messages (they're detailed!)
4. Consult AZURE_OPENAI_GUIDE.md
5. Check conversation history limits

## 📈 Next Steps After Setup

1. ✅ Verify setup with `setup_check.py`
2. ✅ Test basic conversation
3. ✅ Try budget calculation
4. ✅ Request itinerary creation
5. ✅ Explore different destinations
6. ✅ Test AI insights

---

**Version**: 1.0.0  
**Python**: 3.8+  
**Dependencies**: requests, python-dotenv  
**AI**: Azure OpenAI with Azure AD authentication

#!/usr/bin/env python3
"""
Quick test script for Azure OpenAI credentials
"""
import os
from dotenv import load_dotenv


def test_credentials():
    """Test Azure OpenAI credentials"""
    print("=" * 60)
    print("  Azure OpenAI Credentials Test")
    print("=" * 60)
    
    # Load environment
    load_dotenv()
    
    print("\n1. Loading credentials from .env...")
    
    credentials = {
        'OPENAI_ENDPOINT': os.getenv('OPENAI_ENDPOINT', ''),
        'TENANT_ID': os.getenv('TENANT_ID', ''),
        'CLIENT_ID': os.getenv('CLIENT_ID', ''),
        'CLIENT_SECRET': os.getenv('CLIENT_SECRET', ''),
        'OPENAI_DEPLOYMENT': os.getenv('OPENAI_DEPLOYMENT', 'gpt-4')
    }
    
    # Check credentials
    all_present = True
    for key, value in credentials.items():
        if not value or 'your-' in value.lower():
            print(f"   ❌ {key}: Not configured")
            all_present = False
        else:
            if 'SECRET' in key:
                display = value[:8] + '...' if len(value) > 8 else '***'
            else:
                display = value
            print(f"   ✅ {key}: {display}")
    
    if not all_present:
        print("\n❌ Some credentials are missing or have placeholder values")
        print("   Please update your .env file with actual values")
        return False
    
    print("\n2. Testing Azure AD authentication...")
    
    try:
        import requests
        
        token_url = os.getenv('TOKEN_URL')
        token_scope = os.getenv('TOKEN_SCOPE')
        
        payload = {
            'grant_type': 'client_credentials',
            'client_id': credentials['CLIENT_ID'],
            'client_secret': credentials['CLIENT_SECRET'],
            'scope': token_scope
        }
        
        response = requests.post(token_url, data=payload, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Successfully obtained Azure AD token")
            token_data = response.json()
            print(f"   Token expires in: {token_data.get('expires_in', 'unknown')} seconds")
        else:
            print(f"   ❌ Failed to obtain token: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error during authentication: {e}")
        return False
    
    print("\n3. Testing Azure OpenAI API call...")
    
    try:
        from services.azure_openai_client import get_openai_client
        
        client = get_openai_client()
        
        messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'Say "Test successful!" if you receive this message.'}
        ]
        
        response = client.chat_completion(messages, max_tokens=50)
        content = client.get_response_content(response)
        
        print(f"   ✅ API call successful!")
        print(f"   Response: {content}")
        
    except Exception as e:
        print(f"   ❌ API call failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Your Azure OpenAI setup is working.")
    print("=" * 60)
    
    return True


if __name__ == '__main__':
    import sys
    
    try:
        success = test_credentials()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

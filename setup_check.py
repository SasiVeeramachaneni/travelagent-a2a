#!/usr/bin/env python3
"""
Setup and test script for Travel Agent
"""
import os
import sys
from dotenv import load_dotenv


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_dependencies():
    """Check if required dependencies are installed"""
    print("\nChecking dependencies...")
    
    required = {
        'requests': 'requests',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("   Install with: pip install -r requirements.txt")
        return False
    
    return True


def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\nChecking .env configuration...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   Copy .env.example to .env and configure your credentials")
        if os.path.exists('.env.example'):
            print("   Command: cp .env.example .env")
        return False
    
    print("✅ .env file exists")
    
    # Load and check variables
    load_dotenv()
    
    required_vars = {
        'OPENAI_ENDPOINT': 'Azure OpenAI Endpoint',
        'TENANT_ID': 'Azure Tenant ID',
        'CLIENT_ID': 'Azure Client ID',
        'CLIENT_SECRET': 'Azure Client Secret',
        'TOKEN_URL': 'Azure Token URL',
        'TOKEN_SCOPE': 'Azure Token Scope',
        'OPENAI_DEPLOYMENT': 'OpenAI Deployment Name'
    }
    
    missing = []
    placeholder_values = ['your-', 'http://example.com', 'https://example.com']
    
    for var, description in required_vars.items():
        value = os.getenv(var, '')
        if not value:
            print(f"❌ {var} is not set")
            missing.append(var)
        elif any(placeholder in value.lower() for placeholder in placeholder_values):
            print(f"⚠️  {var} appears to have a placeholder value")
            missing.append(var)
        else:
            # Mask sensitive values
            if 'SECRET' in var or 'KEY' in var:
                display_value = value[:8] + '...' if len(value) > 8 else '***'
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
    
    if missing:
        print(f"\n⚠️  Configuration incomplete. Please update these in .env:")
        for var in missing:
            print(f"   - {var}")
        return False
    
    return True


def test_azure_connection():
    """Test connection to Azure OpenAI"""
    print("\nTesting Azure OpenAI connection...")
    
    try:
        from services.azure_openai_client import get_openai_client
        
        client = get_openai_client()
        
        if client.test_connection():
            print("✅ Successfully connected to Azure OpenAI!")
            return True
        else:
            print("❌ Connection test failed")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False


def main():
    """Run setup checks"""
    print("=" * 60)
    print("  Travel Agent - Setup & Configuration Check")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment Configuration", check_env_file),
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Error during {name} check: {e}")
            results.append(False)
    
    # Only test connection if other checks pass
    if all(results):
        results.append(test_azure_connection())
    
    print("\n" + "=" * 60)
    
    if all(results):
        print("✅ All checks passed! You're ready to run the Travel Agent.")
        print("\nTo start the agent, run:")
        print("  python main.py")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nFor help, see README.md")
        return 1


if __name__ == '__main__':
    sys.exit(main())

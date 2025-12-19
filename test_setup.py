"""
Test script for WhatsApp Flows Server

Run this to verify your setup is working correctly.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()


def check_environment_variables():
    """Check if all required environment variables are set"""
    required_vars = [
        "APP_SECRET",
        "PRIVATE_KEY",
        "PASSPHRASE",
        "PORT"
    ]
    
    optional_vars = [
        "WHATSAPP_ACCESS_TOKEN",
        "WHATSAPP_PHONE_NUMBER_ID",
        "WHATSAPP_WABA_ID",
        "WHATSAPP_FLOW_ID"
    ]
    
    print("=" * 60)
    print("🔍 Checking Environment Variables")
    print("=" * 60)
    
    all_set = True
    
    print("\n📋 Required Variables (for Flow Endpoint Server):")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            display_value = "***" if "KEY" in var or "SECRET" in var or "PASS" in var else value[:20] + "..." if len(value) > 20 else value
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ❌ {var}: NOT SET")
            all_set = False
    
    print("\n📋 Optional Variables (for sending messages):")
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            display_value = "***" if "TOKEN" in var else value
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ⚠️  {var}: NOT SET (optional)")
    
    return all_set


def check_dependencies():
    """Check if all required packages are installed"""
    print("\n" + "=" * 60)
    print("📦 Checking Python Dependencies")
    print("=" * 60 + "\n")
    
    packages = [
        "fastapi",
        "uvicorn",
        "cryptography",
        "dotenv",
        "pydantic",
        "requests"
    ]
    
    all_installed = True
    
    for package in packages:
        try:
            if package == "dotenv":
                __import__("dotenv")
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT INSTALLED")
            all_installed = False
    
    if not all_installed:
        print("\n⚠️  Install missing packages with:")
        print("   pip install -r requirements.txt")
    
    return all_installed


def check_files():
    """Check if all required files exist"""
    print("\n" + "=" * 60)
    print("📁 Checking Required Files")
    print("=" * 60 + "\n")
    
    required_files = [
        "server.py",
        "encryption.py",
        "flow.py",
        "key_generator.py",
        "whatsapp_api.py",
        "requirements.txt",
        ".env"
    ]
    
    all_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - NOT FOUND")
            all_exist = False
            
            if file == ".env":
                print("     💡 Copy .env.example to .env and fill in your values")
    
    return all_exist


def test_encryption():
    """Test encryption/decryption functions"""
    print("\n" + "=" * 60)
    print("🔐 Testing Encryption/Decryption")
    print("=" * 60 + "\n")
    
    try:
        from encryption import encrypt_response, decrypt_request
        print("  ✅ Encryption module imported successfully")
        
        # Test data
        test_response = {"test": "data"}
        test_aes_key = b"0123456789abcdef"  # 16 bytes
        test_iv = b"fedcba9876543210"  # 16 bytes
        
        # Test encryption
        encrypted = encrypt_response(test_response, test_aes_key, test_iv)
        print(f"  ✅ Encryption test passed (output: {encrypted[:20]}...)")
        
        return True
    except Exception as e:
        print(f"  ❌ Encryption test failed: {e}")
        return False


def test_api_client():
    """Test WhatsApp API client"""
    print("\n" + "=" * 60)
    print("📡 Testing WhatsApp API Client")
    print("=" * 60 + "\n")
    
    try:
        # Check if access token is set
        if not os.getenv("WHATSAPP_ACCESS_TOKEN"):
            print("  ⚠️  WHATSAPP_ACCESS_TOKEN not set - skipping API tests")
            print("     Set it in .env to test API client")
            return True
        
        from whatsapp_api import WhatsAppCloudAPI, WhatsAppFlowsAPI
        
        print("  ✅ API client modules imported successfully")
        
        # Try to initialize clients
        api = WhatsAppCloudAPI()
        print("  ✅ WhatsApp Cloud API client initialized")
        
        if os.getenv("WHATSAPP_WABA_ID"):
            flows_api = WhatsAppFlowsAPI()
            print("  ✅ WhatsApp Flows API client initialized")
        else:
            print("  ⚠️  WHATSAPP_WABA_ID not set - Flows API not tested")
        
        return True
    except ValueError as e:
        print(f"  ⚠️  {e}")
        print("     This is expected if you haven't set all API credentials yet")
        return True
    except Exception as e:
        print(f"  ❌ API client test failed: {e}")
        return False


def print_next_steps(all_checks_passed):
    """Print next steps based on test results"""
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("✅ All Checks Passed!")
    else:
        print("⚠️  Some Checks Failed")
    print("=" * 60 + "\n")
    
    if all_checks_passed:
        print("🚀 You're ready to start the server!\n")
        print("Run one of these commands:")
        print("  • python server.py")
        print("  • uvicorn server:app --reload --port 3000")
        print("\nThen test with:")
        print("  • curl http://localhost:3000/health")
        print("  • Open http://localhost:3000/docs for API documentation")
        print("\n📖 Read QUICKSTART.md for detailed setup instructions")
    else:
        print("⚠️  Please fix the issues above before starting the server\n")
        print("💡 Quick fixes:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Copy .env.example to .env")
        print("  3. Generate keys: python key_generator.py YourPassphrase")
        print("  4. Fill in .env with your credentials")
        print("\n📖 See QUICKSTART.md for step-by-step instructions")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "WhatsApp Flows Server - Setup Test" + " " * 13 + "║")
    print("╚" + "=" * 58 + "╝")
    
    checks = [
        ("Files", check_files()),
        ("Dependencies", check_dependencies()),
        ("Environment", check_environment_variables()),
        ("Encryption", test_encryption()),
        ("API Client", test_api_client())
    ]
    
    all_passed = all(result for _, result in checks)
    
    print_next_steps(all_passed)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Setup Gemini API Key"""

import os

def setup_gemini_key():
    print("Gemini API Key Setup")
    print("=" * 20)
    print("Get your free API key from: https://makersuite.google.com/app/apikey")
    print("Options:")
    print("1. Enter API key (for full LLM features)")
    print("2. Skip (use fallback mode)")
    
    choice = input("\nChoose (1/2): ")
    
    if choice == "1":
        api_key = input("Enter your Gemini API key: ").strip()
        if api_key:
            # Set environment variable for current session
            os.environ['GEMINI_API_KEY'] = api_key
            
            # Create .env file
            with open('.env', 'w') as f:
                f.write(f'GEMINI_API_KEY={api_key}\n')
            
            print("[OK] API key saved!")
            print("[OK] Full LLM features enabled")
            return True
        else:
            print("No API key entered")
    
    print("Using fallback mode (pattern matching)")
    return False

if __name__ == "__main__":
    setup_gemini_key()
    print("\nNow run: python chatbot/app.py")
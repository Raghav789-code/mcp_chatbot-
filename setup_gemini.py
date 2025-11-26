#!/usr/bin/env python3
"""Easy Gemini API Key Setup"""

import os

def setup_gemini():
    print("=" * 50)
    print("GEMINI API KEY SETUP")
    print("=" * 50)
    print()
    print("1. Get your FREE Gemini API key:")
    print("   https://makersuite.google.com/app/apikey")
    print()
    print("2. Copy your API key")
    print()
    
    api_key = input("3. Paste your Gemini API key here: ").strip()
    
    if api_key and api_key != "your_gemini_api_key_here":
        # Update .env file
        with open('.env', 'w') as f:
            f.write(f'GEMINI_API_KEY={api_key}\n')
        
        print()
        print("✅ SUCCESS! API key saved to .env file")
        print("✅ Full Gemini AI features enabled")
        print()
        print("Now run: python chatbot/app.py")
        print("Browser will open automatically!")
        
    else:
        print()
        print("❌ No valid API key entered")
        print("The chatbot will run in fallback mode")
        print()
        print("Run: python chatbot/app.py")
        print("Browser will open automatically!")

if __name__ == "__main__":
    setup_gemini()
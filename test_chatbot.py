#!/usr/bin/env python3
"""Test script to verify chatbot setup"""

import os
import sys

def check_files():
    """Check if all required files exist"""
    required_files = [
        'chatbot/app.py',
        'templates/chat.html',
        'chatbot_requirements.txt',
        'people_server/main.py',
        'people_server/data.py'
    ]
    
    print("Checking required files...")
    all_good = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"[OK] {file_path}")
        else:
            print(f"[MISSING] {file_path}")
            all_good = False
    
    return all_good

def test_imports():
    """Test if all required modules can be imported"""
    print("\nTesting imports...")
    
    try:
        import fastapi
        print("[OK] FastAPI imported")
    except ImportError:
        print("[ERROR] FastAPI not installed")
        return False
    
    try:
        import uvicorn
        print("[OK] Uvicorn imported")
    except ImportError:
        print("[ERROR] Uvicorn not installed")
        return False
    
    try:
        import websockets
        print("[OK] WebSockets imported")
    except ImportError:
        print("[ERROR] WebSockets not installed")
        return False
    
    try:
        from people_server.data import get_people_data
        people = get_people_data()
        print(f"[OK] MCP server data loaded ({len(people)} people)")
    except ImportError:
        print("[ERROR] Cannot import MCP server modules")
        return False
    
    return True

if __name__ == "__main__":
    print("People Directory Chatbot - Setup Test")
    print("=" * 45)
    
    files_ok = check_files()
    imports_ok = test_imports()
    
    print("\n" + "=" * 45)
    
    if files_ok and imports_ok:
        print("[SUCCESS] All checks passed!")
        print("\nTo start the chatbot:")
        print("1. Run: python chatbot/app.py")
        print("2. Open: http://localhost:8000")
        print("3. Or double-click: start_chatbot.bat")
    else:
        print("[ERROR] Some checks failed. Please fix the issues above.")
        sys.exit(1)
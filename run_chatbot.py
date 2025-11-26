#!/usr/bin/env python3
"""Launch script for the chatbot interface"""

import subprocess
import sys
import os
import time

def install_requirements():
    """Install chatbot requirements"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'chatbot_requirements.txt'])
        print("[OK] Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install dependencies: {e}")
        sys.exit(1)

def run_chatbot():
    """Run the chatbot server"""
    try:
        print("[INFO] Starting chatbot server...")
        print("[INFO] Open http://localhost:8000 in your browser")
        print("[INFO] Press Ctrl+C to stop")
        
        subprocess.run([sys.executable, 'chatbot/app.py'])
    except KeyboardInterrupt:
        print("\n[INFO] Chatbot server stopped")
    except Exception as e:
        print(f"[ERROR] Error running chatbot: {e}")

if __name__ == "__main__":
    print("People Directory Chatbot Setup")
    print("=" * 40)
    
    install_requirements()
    run_chatbot()
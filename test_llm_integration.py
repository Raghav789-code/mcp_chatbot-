#!/usr/bin/env python3
"""Test LLM Integration"""

import asyncio
import os
from chatbot.llm_client import LLMClient

class MockMCPClient:
    async def call_tool(self, tool_name, arguments=None):
        return f"Mock result for {tool_name} with args: {arguments}"

async def test_llm():
    print("Testing LLM Integration")
    print("=" * 25)
    
    # Test without API key (fallback mode)
    llm_client = LLMClient()
    mcp_client = MockMCPClient()
    
    test_messages = [
        "santosh",
        "David Johnson",
        "Find Sarah",
        "List all managers",
        "Details of John Smith"
    ]
    
    for message in test_messages:
        print(f"\nTesting: '{message}'")
        response = await llm_client.process_message(message, mcp_client)
        print(f"Response: {response[:100]}...")
    
    print("\n[SUCCESS] LLM integration working!")
    
    # Check if API key is available
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("[INFO] Gemini API key found - full LLM features available")
    else:
        print("[INFO] No API key - using fallback mode")
        print("Run 'python setup_openai.py' to add API key")

if __name__ == "__main__":
    asyncio.run(test_llm())
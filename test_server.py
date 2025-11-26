#!/usr/bin/env python3
"""Quick test to verify MCP server imports work"""

try:
    from people_server.main import server
    from people_server.data import get_people_data
    from people_server.fuzzy import fuzzy_search_people
    
    print("[OK] All imports successful")
    print("[OK] Server object created")
    
    # Test data loading
    people = get_people_data()
    print(f"[OK] Loaded {len(people)} people from dataset")
    
    # Test fuzzy search
    results = fuzzy_search_people(people, "Ayush", 3)
    print(f"[OK] Fuzzy search working - found {len(results['candidates'])} candidates")
    
    print("\n[SUCCESS] MCP Server is ready to run!")
    print("Run with: python -m people_server.main")
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
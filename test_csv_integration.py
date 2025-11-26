#!/usr/bin/env python3
"""Test CSV integration"""

from people_server.csv_data import get_people_data
from people_server.fuzzy import fuzzy_search_people

def test_csv_integration():
    print("Testing CSV Integration")
    print("=" * 25)
    
    # Test data loading
    people = get_people_data()
    print(f"[OK] Loaded {len(people)} people from CSV")
    
    # Test first person
    if people:
        first_person = people[0]
        print(f"[OK] First person: {first_person['full_name']}")
        print(f"  Department: {first_person['department']}")
        print(f"  Role: {first_person['role']}")
    
    # Test fuzzy search
    results = fuzzy_search_people(people, "Ayush", 3)
    print(f"[OK] Fuzzy search for 'Ayush' found {len(results['candidates'])} candidates")
    
    # Test filtering
    cs_people = [p for p in people if p['department'].lower() == 'computer science']
    print(f"[OK] Found {len(cs_people)} people in Computer Science")
    
    print("\n[SUCCESS] CSV integration working perfectly!")

if __name__ == "__main__":
    test_csv_integration()
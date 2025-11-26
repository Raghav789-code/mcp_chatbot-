#!/usr/bin/env python3
"""Local testing script for People Directory MCP tools"""

import json
from people_server.data import get_people_data
from people_server.fuzzy import fuzzy_search_people

def test_exact_search():
    """Test exact name search functionality"""
    print("=== Testing Exact Search ===")
    people = get_people_data()
    
    test_cases = ["Ayush", "ayush sharma", "Dr. Priya Patel", "NonExistent"]
    
    for test_name in test_cases:
        print(f"\nSearching for: '{test_name}'")
        matches = []
        search_name = test_name.lower()
        
        for person in people:
            if (person["full_name"].lower() == search_name or 
                person["preferred_name"].lower() == search_name):
                matches.append(person)
        
        if matches:
            print(f"Found {len(matches)} match(es):")
            for match in matches:
                print(f"  - {match['full_name']} ({match['preferred_name']})")
        else:
            print("No exact matches found")

def test_fuzzy_search():
    """Test fuzzy search functionality"""
    print("\n=== Testing Fuzzy Search ===")
    people = get_people_data()
    
    test_cases = ["Ayshu", "Aysuh", "Prya", "Rahool", "Srah"]
    
    for test_name in test_cases:
        print(f"\nFuzzy searching for: '{test_name}'")
        results = fuzzy_search_people(people, test_name, 3)
        
        if results["candidates"]:
            best = results["candidates"][0]
            print(f"Best match: {best['matched_name']} (similarity: {best['similarity']:.2f})")
            
            if best["similarity"] > 0.85:
                print("  -> High confidence match")
            elif best["similarity"] < 0.6:
                print("  -> Low confidence match")
            
            print("All candidates:")
            for candidate in results["candidates"]:
                print(f"  - {candidate['matched_name']}: {candidate['similarity']:.2f}")
        else:
            print("No candidates found")

def test_list_people():
    """Test people listing with filters"""
    print("\n=== Testing List People ===")
    people = get_people_data()
    
    test_filters = [
        {"department": "Computer Science"},
        {"role": "Student"},
        {"location": "Delhi Campus"},
        {"department": "Data Science", "role": "Professor"},
        {}  # No filters
    ]
    
    for filters in test_filters:
        print(f"\nFiltering with: {filters}")
        
        filtered = people.copy()
        if "department" in filters:
            filtered = [p for p in filtered if p["department"].lower() == filters["department"].lower()]
        if "role" in filters:
            filtered = [p for p in filtered if p["role"].lower() == filters["role"].lower()]
        if "location" in filters:
            filtered = [p for p in filtered if p["location"].lower() == filters["location"].lower()]
        
        print(f"Found {len(filtered)} people:")
        for person in filtered:
            print(f"  - {person['full_name']} - {person['role']} in {person['department']}")

if __name__ == "__main__":
    print("People Directory MCP Server - Local Testing")
    print("=" * 50)
    
    test_exact_search()
    test_fuzzy_search() 
    test_list_people()
    
    print("\n" + "=" * 50)
    print("Testing complete!")
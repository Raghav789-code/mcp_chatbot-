#!/usr/bin/env python3
"""Test backend search directly"""

import sys
import os
sys.path.append('people_server')

from csv_data import get_people_data
from fuzzy import fuzzy_search_people

def test_search():
    print("Testing backend search...")
    
    # Load data
    people_data = get_people_data()
    print(f"Loaded {len(people_data)} people")
    
    # Test search for "raghav"
    print("\nSearching for 'raghav':")
    results = fuzzy_search_people(people_data, "raghav", 5)
    if results["candidates"]:
        for candidate in results["candidates"]:
            person = candidate["person"]
            print(f"- {person['full_name']} (ID: {person['id']})")
    else:
        print("No employees found with name 'raghav'")
    
    # Test search for "karen"
    print("\nSearching for 'karen':")
    results = fuzzy_search_people(people_data, "karen", 5)
    if results["candidates"]:
        for candidate in results["candidates"]:
            person = candidate["person"]
            print(f"- {person['full_name']} (ID: {person['id']})")
    else:
        print("No employees found with name 'karen'")

if __name__ == "__main__":
    test_search()
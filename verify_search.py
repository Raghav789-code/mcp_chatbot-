#!/usr/bin/env python3
"""Verify search functionality works correctly"""

import pandas as pd
from people_server.csv_data import get_people_data, reload_csv_data
from people_server.fuzzy import fuzzy_search_people

def main():
    print("Reloading CSV data...")
    reload_csv_data()
    
    print("Getting people data...")
    people_data = get_people_data()
    print(f"Total people loaded: {len(people_data)}")
    
    if len(people_data) == 0:
        print("ERROR: No data loaded!")
        return
    
    # Show sample of data structure
    print(f"\nSample person data structure:")
    sample = people_data[0]
    for key, value in sample.items():
        print(f"  {key}: {value}")
    
    # Search for names containing "shiv" (case insensitive)
    print(f"\n{'='*60}")
    print("Searching for people with 'shiv' in their name...")
    
    # Manual search first to verify data
    shiv_people = []
    for person in people_data:
        if 'shiv' in person['full_name'].lower():
            shiv_people.append(person)
    
    print(f"Manual search found {len(shiv_people)} people with 'shiv' in name:")
    for person in shiv_people[:5]:  # Show first 5
        print(f"  - {person['full_name']} (ID: {person['id']}) - {person['role']} in {person['department']}")
    
    # Now test fuzzy search
    print(f"\nFuzzy search results for 'shiv':")
    results = fuzzy_search_people(people_data, "shiv", max_results=5)
    
    for i, candidate in enumerate(results['candidates']):
        person = candidate['person']
        similarity = candidate['similarity']
        print(f"  {i+1}. {person['full_name']} - Similarity: {similarity:.1%}")
        print(f"     Role: {person['role']} | Department: {person['department']}")

if __name__ == "__main__":
    main()
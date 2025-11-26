#!/usr/bin/env python3
"""Test script to verify search functionality"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'people_server'))

from csv_data import get_people_data
from fuzzy import fuzzy_search_people

def test_search():
    print("Loading data...")
    people_data = get_people_data()
    print(f"Loaded {len(people_data)} people")
    
    # Show first few people to verify data structure
    print("\nFirst 3 people:")
    for i, person in enumerate(people_data[:3]):
        print(f"{i+1}. {person['full_name']} - {person['role']} in {person['department']}")
    
    # Test search for "shiv"
    print("\n" + "="*50)
    print("Testing search for 'shiv':")
    results = fuzzy_search_people(people_data, "shiv", max_results=5)
    
    print(f"Query: {results['query']}")
    print(f"Found {len(results['candidates'])} candidates:")
    
    for i, candidate in enumerate(results['candidates']):
        person = candidate['person']
        similarity = candidate['similarity']
        print(f"{i+1}. {person['full_name']} - Similarity: {similarity:.2%}")
        print(f"   Role: {person['role']} | Department: {person['department']}")
    
    # Test search for "Rohit"
    print("\n" + "="*50)
    print("Testing search for 'Rohit':")
    results = fuzzy_search_people(people_data, "Rohit", max_results=5)
    
    print(f"Query: {results['query']}")
    print(f"Found {len(results['candidates'])} candidates:")
    
    for i, candidate in enumerate(results['candidates']):
        person = candidate['person']
        similarity = candidate['similarity']
        print(f"{i+1}. {person['full_name']} - Similarity: {similarity:.2%}")
        print(f"   Role: {person['role']} | Department: {person['department']}")

if __name__ == "__main__":
    test_search()
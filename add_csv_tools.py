#!/usr/bin/env python3
"""Tool to add new people to CSV and manage CSV data"""

from people_server.csv_data import add_person_to_csv, reload_csv_data, get_people_data
import pandas as pd

def add_new_person():
    """Interactive tool to add new person to CSV"""
    print("Add New Person to CSV")
    print("=" * 25)
    
    person_data = {
        "id": int(input("ID: ")),
        "full_name": input("Full Name: "),
        "preferred_name": input("Preferred Name: "),
        "email": input("Email: "),
        "phone": input("Phone: "),
        "role": input("Role: "),
        "department": input("Department: "),
        "location": input("Location: "),
        "tags": input("Tags (comma-separated): ")
    }
    
    add_person_to_csv(person_data)
    print("Person added successfully!")

def view_csv_data():
    """View current CSV data"""
    people = get_people_data()
    print(f"\nCurrent CSV Data ({len(people)} people):")
    print("=" * 40)
    
    for person in people:
        print(f"ID: {person['id']} | {person['full_name']} ({person['preferred_name']}) | {person['role']} | {person['department']}")

def create_custom_csv():
    """Create a custom CSV file"""
    print("Create Custom CSV File")
    print("=" * 22)
    
    filename = input("Enter CSV filename (e.g., employees.csv): ")
    
    # Sample data for different types
    templates = {
        "employees": [
            {"id": 1, "full_name": "John Doe", "preferred_name": "John", "email": "john@company.com", 
             "phone": "+1-555-0001", "role": "Manager", "department": "Sales", "location": "New York", "tags": "leadership,sales"},
            {"id": 2, "full_name": "Jane Smith", "preferred_name": "Jane", "email": "jane@company.com", 
             "phone": "+1-555-0002", "role": "Developer", "department": "Engineering", "location": "San Francisco", "tags": "python,web-dev"}
        ],
        "students": [
            {"id": 1, "full_name": "Alice Johnson", "preferred_name": "Alice", "email": "alice@school.edu", 
             "phone": "+1-555-1001", "role": "Student", "department": "Mathematics", "location": "Campus A", "tags": "calculus,algebra"},
            {"id": 2, "full_name": "Bob Wilson", "preferred_name": "Bob", "email": "bob@school.edu", 
             "phone": "+1-555-1002", "role": "Student", "department": "Physics", "location": "Campus B", "tags": "quantum,mechanics"}
        ]
    }
    
    template_type = input("Choose template (employees/students/custom): ").lower()
    
    if template_type in templates:
        data = templates[template_type]
    else:
        print("Creating empty template...")
        data = [
            {"id": 1, "full_name": "Sample Name", "preferred_name": "Sample", "email": "sample@example.com", 
             "phone": "+1-555-0000", "role": "Role", "department": "Department", "location": "Location", "tags": "tag1,tag2"}
        ]
    
    df = pd.DataFrame(data)
    filepath = f"data/{filename}"
    df.to_csv(filepath, index=False)
    print(f"Created CSV file: {filepath}")

if __name__ == "__main__":
    while True:
        print("\nCSV Management Tool")
        print("=" * 20)
        print("1. View current data")
        print("2. Add new person")
        print("3. Create custom CSV")
        print("4. Reload CSV data")
        print("5. Exit")
        
        choice = input("\nChoose option (1-5): ")
        
        if choice == "1":
            view_csv_data()
        elif choice == "2":
            add_new_person()
        elif choice == "3":
            create_custom_csv()
        elif choice == "4":
            reload_csv_data()
            print("CSV data reloaded!")
        elif choice == "5":
            break
        else:
            print("Invalid choice!")
#!/usr/bin/env python3
"""CSV File Selector Tool"""

import os
import glob
import shutil

def list_csv_files():
    """List all CSV files in data directory"""
    csv_files = glob.glob("data/*.csv")
    
    if not csv_files:
        print("No CSV files found in data/ directory")
        return []
    
    print("Available CSV files:")
    for i, file in enumerate(csv_files, 1):
        filename = os.path.basename(file)
        print(f"{i}. {filename}")
    
    return csv_files

def select_csv_file():
    """Interactive CSV file selector"""
    csv_files = list_csv_files()
    
    if not csv_files:
        return None
    
    while True:
        try:
            choice = int(input(f"\nSelect CSV file (1-{len(csv_files)}): ")) - 1
            if 0 <= choice < len(csv_files):
                selected_file = csv_files[choice]
                print(f"Selected: {os.path.basename(selected_file)}")
                return selected_file
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a number!")

def preview_csv(file_path):
    """Preview CSV file contents"""
    import pandas as pd
    
    try:
        df = pd.read_csv(file_path)
        print(f"\nPreview of {os.path.basename(file_path)}:")
        print("=" * 50)
        print(f"Rows: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst 3 rows:")
        print(df.head(3).to_string(index=False))
    except Exception as e:
        print(f"Error reading CSV: {e}")

def set_primary_csv(file_path):
    """Set a CSV file as the primary one (rename to people.csv)"""
    primary_path = "data/people.csv"
    
    if file_path != primary_path:
        # Backup existing people.csv if it exists
        if os.path.exists(primary_path):
            backup_path = "data/people_backup.csv"
            shutil.copy2(primary_path, backup_path)
            print(f"Backed up existing people.csv to people_backup.csv")
        
        # Copy selected file to people.csv
        shutil.copy2(file_path, primary_path)
        print(f"Set {os.path.basename(file_path)} as primary CSV file")

if __name__ == "__main__":
    print("CSV File Selector")
    print("=" * 20)
    
    while True:
        print("\n1. List CSV files")
        print("2. Preview CSV file")
        print("3. Set primary CSV file")
        print("4. Exit")
        
        choice = input("\nChoose option (1-4): ")
        
        if choice == "1":
            list_csv_files()
        elif choice == "2":
            selected = select_csv_file()
            if selected:
                preview_csv(selected)
        elif choice == "3":
            selected = select_csv_file()
            if selected:
                set_primary_csv(selected)
        elif choice == "4":
            break
        else:
            print("Invalid choice!")
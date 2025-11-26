"""Simple CSV Data Handler"""

import pandas as pd
import os
from typing import List, Dict, Any

def get_people_data() -> List[Dict[str, Any]]:
    """Load and return employee data"""
    csv_path = "data/Employee_Complete_Dataset.csv"
    
    if not os.path.exists(csv_path):
        return []
    
    try:
        df = pd.read_csv(csv_path)
        people_list = []
        
        for _, row in df.iterrows():
            person = {
                "id": int(row['Employee_number']),
                "full_name": str(row['Employee_name']),
                "preferred_name": str(row['Employee_name']).split()[0],
                "email": f"{str(row['Employee_name']).lower().replace(' ', '.')}@company.com",
                "phone": "+91-9876543210",
                "role": str(row['Role']),
                "department": str(row['Department']),
                "location": "Office",
                "tags": []
            }
            people_list.append(person)
        
        return people_list
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []

def reload_csv_data():
    """Reload data - no-op for simple implementation"""
    pass
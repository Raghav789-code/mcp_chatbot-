import pandas as pd
import os

def load_employee_data():
    """Load employee data from CSV"""
    csv_path = "data/Employee_Complete_Dataset.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        return df
    return None

def search_employees(query):
    """Search employees by name"""
    df = load_employee_data()
    if df is None:
        return []
    
    query = query.lower().strip()
    results = []
    
    # Search in Employee_name column
    for _, row in df.iterrows():
        name = str(row['Employee_name']).lower()
        if query in name:
            results.append({
                'id': row['Employee_number'],
                'name': row['Employee_name'],
                'role': row['Role'],
                'department': row['Department'],
                'age': row['Employee_age'],
                'salary': row['Current_Salary']
            })
    
    return results[:5]  # Return top 5 matches

# Test the search
if __name__ == "__main__":
    results = search_employees("john")
    print(f"Found {len(results)} employees:")
    for emp in results:
        print(f"- {emp['name']} (ID: {emp['id']}) - {emp['role']} in {emp['department']}")
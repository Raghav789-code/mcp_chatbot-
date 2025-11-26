"""Simple name search"""

from typing import List, Dict, Any

def fuzzy_search_people(people_data: List[Dict[str, Any]], query: str, max_results: int = 3) -> Dict[str, Any]:
    """Simple name search"""
    query = query.lower().strip()
    matches = []
    
    for person in people_data:
        name = person["full_name"].lower()
        
        # Simple substring search
        if query in name:
            matches.append({
                "similarity": 1.0,
                "matched_name": person["full_name"],
                "person": person
            })
    
    return {
        "query": query,
        "best_match": matches[0]["matched_name"] if matches else None,
        "candidates": matches[:max_results]
    }
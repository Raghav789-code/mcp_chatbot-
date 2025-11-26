# People Directory MCP Server

A Python-based MCP (Model Context Protocol) server that provides tools to query a People Directory with exact and fuzzy name search capabilities.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run MCP Server
```bash
python -m people_server.main
```

### Test Locally
```bash
python local_test.py
```

## Available Tools

- **ping**: Health check returning "pong" with timestamp
- **get_person_exact**: Exact name lookup (case-insensitive)
- **get_person_fuzzy**: Fuzzy/typo-tolerant name search using rapidfuzz
- **list_people**: Filter people by department/role/location

## Data Structure

Each person has: id, full_name, preferred_name, email, phone, role, department, location, tags.

Sample data includes people with similar names for testing fuzzy search:
- "Ayush Sharma" vs "Aayush Jain"
- Various departments: Computer Science, Data Science, etc.
- Multiple locations: Delhi Campus, Mumbai Office, etc.

## Fuzzy Search Behavior

- Similarity scores: 0-1 scale
- High confidence: >0.85 (treat as intended person)
- Low confidence: <0.6 (no close match)
- Default max results: 3

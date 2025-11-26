from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
import json
import subprocess
import sqlite3
import os
from datetime import datetime
from typing import Dict, List
from llm_client import LLMClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def init_db():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            message TEXT,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class MCPClient:
    def __init__(self):
        # Import here to avoid circular imports
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        
        from people_server.csv_data import get_people_data, reload_csv_data
        from people_server.fuzzy import fuzzy_search_people
        
        # Reload data to ensure we have the latest
        reload_csv_data()
        
        self.get_people_data = get_people_data
        self.fuzzy_search_people = fuzzy_search_people
    
    async def call_tool(self, tool_name: str, arguments: dict = None):
        """Call MCP tools directly without subprocess"""
        try:
            if arguments is None:
                arguments = {}
            
            # Force reload data every time
            import pandas as pd
            import os
            csv_path = "data/Employee_Complete_Dataset.csv"
            people_data = []
            
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
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
                    people_data.append(person)
            
            if tool_name == "ping":
                from datetime import datetime
                timestamp = datetime.now().isoformat()
                return f"pong - {timestamp}"
            
            elif tool_name == "get_person_exact":
                search_name = arguments.get("name", "").lower()
                matches = []
                
                for person in people_data:
                    if (person["full_name"].lower() == search_name or 
                        person["preferred_name"].lower() == search_name):
                        matches.append(person)
                
                if not matches:
                    return f"No employee found with exact name '{arguments.get('name')}'"
                
                result_text = f"Found {len(matches)} exact match(es) for '{arguments.get('name')}':\n\n"
                for person in matches:
                    result_text += f"- {person['full_name']} (ID: {person['id']}) - {person['role']} in {person['department']}\n"
                    result_text += f"  Email: {person['email']} | Phone: {person['phone']}\n\n"
                
                return result_text
            
            elif tool_name == "get_person_fuzzy":
                search_name = arguments.get("name", "").lower().strip()
                max_results = arguments.get("maxResults", 5)
                
                # Direct search in employee names
                matches = []
                for person in people_data:
                    if search_name in person["full_name"].lower():
                        matches.append(person)
                
                if not matches:
                    return f"No employees found with name '{arguments.get('name')}'"
                
                matches = matches[:max_results]
                result_text = f"Found {len(matches)} employee(s) with '{arguments.get('name')}':\n\n"
                
                for i, person in enumerate(matches, 1):
                    result_text += f"{i}. {person['full_name']} (ID: {person['id']})\n"
                    result_text += f"   Role: {person['role']} | Department: {person['department']}\n"
                    result_text += f"   Email: {person['email']} | Phone: {person['phone']}\n\n"
                
                return result_text
            
            elif tool_name == "list_people":
                department = arguments.get("department")
                role = arguments.get("role") 
                min_salary = arguments.get("min_salary")
                max_salary = arguments.get("max_salary")
                min_age = arguments.get("min_age")
                max_age = arguments.get("max_age")
                limit = arguments.get("limit", 10)
                
                # Filter directly from CSV data
                filtered_people = []
                for _, row in df.iterrows():
                    # Create person with all data
                    person = {
                        "id": int(row['Employee_number']),
                        "full_name": str(row['Employee_name']),
                        "role": str(row['Role']),
                        "department": str(row['Department']),
                        "salary": int(row['Current_Salary']),
                        "age": int(row['Employee_age']),
                        "education": str(row['Education_level'])
                    }
                    
                    # Apply filters
                    if department and department.lower() not in person["department"].lower():
                        continue
                    if role and role.lower() not in person["role"].lower():
                        continue
                    if min_salary and person['salary'] < int(min_salary):
                        continue
                    if max_salary and person['salary'] > int(max_salary):
                        continue
                    if min_age and person['age'] < int(min_age):
                        continue
                    if max_age and person['age'] > int(max_age):
                        continue
                    
                    filtered_people.append(person)
                
                # Sort by salary (highest first)
                filtered_people.sort(key=lambda x: x['salary'], reverse=True)
                filtered_people = filtered_people[:limit]
                
                if not filtered_people:
                    return "No employees found matching the criteria"
                
                filters_used = []
                if department: filters_used.append(f"department: {department}")
                if role: filters_used.append(f"role: {role}")
                if min_salary: filters_used.append(f"salary >= ${min_salary}")
                if max_salary: filters_used.append(f"salary <= ${max_salary}")
                if min_age: filters_used.append(f"age >= {min_age}")
                if max_age: filters_used.append(f"age <= {max_age}")
                
                filter_text = f" with filters: {', '.join(filters_used)}" if filters_used else ""
                result_text = f"Found {len(filtered_people)} employees{filter_text}:\n\n"
                
                for i, person in enumerate(filtered_people, 1):
                    result_text += f"{i}. {person['full_name']} (ID: {person['id']})\n"
                    result_text += f"   Role: {person['role']} | Department: {person['department']}\n"
                    result_text += f"   Age: {person['age']}, Salary: ${person['salary']:,}\n"
                    result_text += f"   Education: {person['education']}\n\n"
                
                return result_text
            
            else:
                return f"Unknown tool: {tool_name}"
                
        except Exception as e:
            return f"Error: {str(e)}"

mcp_client = MCPClient()

# Initialize LLM client (will use fallback mode if no API key)
api_key = os.getenv('GEMINI_API_KEY')
llm_client = LLMClient(api_key)

def save_chat(session_id: str, message: str, response: str):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO chat_sessions (session_id, message, response) VALUES (?, ?, ?)',
        (session_id, message, response)
    )
    conn.commit()
    conn.close()

def get_chat_history(session_id: str) -> List[Dict]:
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT message, response, timestamp FROM chat_sessions WHERE session_id = ? ORDER BY timestamp',
        (session_id,)
    )
    history = []
    for row in cursor.fetchall():
        history.append({
            'message': row[0],
            'response': row[1],
            'timestamp': row[2]
        })
    conn.close()
    return history

async def process_message(message: str) -> str:
    """Process message using LLM client"""
    return await llm_client.process_message(message, mcp_client)

@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    history = get_chat_history(session_id)
    await websocket.send_text(json.dumps({
        "type": "history",
        "data": history
    }))
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data.get('message', '')
            
            if user_message.strip():
                response = await process_message(user_message)
                save_chat(session_id, user_message, response)
                
                await websocket.send_text(json.dumps({
                    "type": "response",
                    "data": {
                        "message": user_message,
                        "response": response,
                        "timestamp": datetime.now().isoformat()
                    }
                }))
    
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading
    import time
    
    import socket
    
    def find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]
    
    port = find_free_port()
    
    def open_browser():
        time.sleep(2)  # Wait for server to start
        webbrowser.open(f'http://localhost:{port}')
    
    print("\n[INFO] Chatbot Server Starting...")
    print(f"[INFO] Using port: {port}")
    print("[INFO] Browser will open automatically...")
    print("[INFO] Press Ctrl+C to stop\n")
    
    # Start browser in separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    uvicorn.run(app, host="0.0.0.0", port=port)
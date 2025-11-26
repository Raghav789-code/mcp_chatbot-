"""LLM Client with MCP Tool Integration using Gemini"""

import json
import asyncio
import google.generativeai as genai
from typing import Dict, List, Any

class LLMClient:
    def __init__(self, api_key: str = None):
        # Use free/demo mode if no API key
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
        
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "ping",
                    "description": "Health check - returns pong with timestamp",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "get_person_exact",
                    "description": "Find people with exact name match",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Name to search for"}
                        },
                        "required": ["name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_person_fuzzy", 
                    "description": "Find people with fuzzy/typo-tolerant name search",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Name to search for"},
                            "maxResults": {"type": "integer", "description": "Max results", "default": 3}
                        },
                        "required": ["name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_people",
                    "description": "List people filtered by department, role, location",
                    "parameters": {
                        "type": "object", 
                        "properties": {
                            "department": {"type": "string", "description": "Filter by department"},
                            "role": {"type": "string", "description": "Filter by role"},
                            "location": {"type": "string", "description": "Filter by location"},
                            "limit": {"type": "integer", "description": "Max results", "default": 20}
                        }
                    }
                }
            }
        ]
    
    async def process_message(self, message: str, mcp_client) -> str:
        """Process message with LLM and handle tool calls"""
        
        if not self.model:
            # Fallback to simple pattern matching if no API key
            return await self._fallback_processing(message, mcp_client)
        
        try:
            # Analyze message with Gemini to determine intent
            prompt = f"""You are a helpful assistant that can search for people in a company directory.
            
Analyze this user message and determine what they want:
            Message: "{message}"
            
            Respond with one of these formats:
            1. To search for a person: SEARCH_PERSON: [name]
            2. To list people by criteria: LIST_PEOPLE: [filters]
            3. For general conversation: CHAT: [your response]
            4. For system check: PING
            
            IMPORTANT: If the query contains words like 'age', 'salary', 'above', 'below', 'over', 'under' followed by numbers, it's a LIST_PEOPLE query, NOT a person search.
            
            Examples:
            - "find john" -> SEARCH_PERSON: john
            - "age above 40" -> LIST_PEOPLE: min_age=40
            - "age below 30" -> LIST_PEOPLE: max_age=30
            - "salary above 50000" -> LIST_PEOPLE: min_salary=50000
            - "salary below 100000" -> LIST_PEOPLE: max_salary=100000
            - "people with age over 35" -> LIST_PEOPLE: min_age=35
            - "employees in sales" -> LIST_PEOPLE: department=Sales
            - "managers" -> LIST_PEOPLE: role=Manager
            - "engineering managers" -> LIST_PEOPLE: department=Engineering,role=Manager
            - "high paid employees" -> LIST_PEOPLE: min_salary=80000
            - "young employees" -> LIST_PEOPLE: max_age=30
            - "senior employees" -> LIST_PEOPLE: min_age=40
            """
            
            response = self.model.generate_content(prompt)
            intent = response.text.strip()
            
            # Process based on intent
            if intent.startswith('SEARCH_PERSON:'):
                name = intent.replace('SEARCH_PERSON:', '').strip()
                result = await mcp_client.call_tool('get_person_fuzzy', {'name': name})
                
                # Format response with Gemini
                format_prompt = f"""Format this search result in a conversational way:
                User asked about: {name}
                Search result: {result}
                
                Make it sound natural and helpful."""
                
                formatted = self.model.generate_content(format_prompt)
                return formatted.text
                
            elif intent.startswith('LIST_PEOPLE:'):
                filters_str = intent.replace('LIST_PEOPLE:', '').strip()
                filters = {}
                
                # Parse various filter types
                if 'role=' in filters_str:
                    role = filters_str.split('role=')[1].split(',')[0].strip()
                    filters['role'] = role
                if 'department=' in filters_str:
                    dept = filters_str.split('department=')[1].split(',')[0].strip()
                    filters['department'] = dept
                if 'min_salary=' in filters_str:
                    min_sal = filters_str.split('min_salary=')[1].split(',')[0].strip()
                    filters['min_salary'] = min_sal
                if 'max_salary=' in filters_str:
                    max_sal = filters_str.split('max_salary=')[1].split(',')[0].strip()
                    filters['max_salary'] = max_sal
                if 'min_age=' in filters_str:
                    min_age = filters_str.split('min_age=')[1].split(',')[0].strip()
                    filters['min_age'] = min_age
                if 'max_age=' in filters_str:
                    max_age = filters_str.split('max_age=')[1].split(',')[0].strip()
                    filters['max_age'] = max_age
                if 'education=' in filters_str:
                    edu = filters_str.split('education=')[1].split(',')[0].strip()
                    filters['education'] = edu
                
                result = await mcp_client.call_tool('list_people', filters)
                
                # Format response with Gemini
                format_prompt = f"""Format this list result in a conversational way:
                User requested: {message}
                List result: {result}
                
                Make it sound natural and helpful."""
                
                formatted = self.model.generate_content(format_prompt)
                return formatted.text
                
            elif intent.startswith('PING'):
                result = await mcp_client.call_tool('ping')
                return result
                
            elif intent.startswith('CHAT:'):
                return intent.replace('CHAT:', '').strip()
                
            else:
                return intent
                
        except Exception as e:
            print(f"Gemini Error: {e}")
            return await self._fallback_processing(message, mcp_client)
    
    async def _fallback_processing(self, message: str, mcp_client) -> str:
        """Simple pattern matching for natural language"""
        message_lower = message.lower().strip()
        
        if 'ping' in message_lower:
            return await mcp_client.call_tool('ping')
        
        import re
        filters = {}
        
        # Age patterns
        age_above = re.search(r'age (?:above|over|greater than) (\d+)', message_lower)
        age_below = re.search(r'age (?:below|under|less than) (\d+)', message_lower)
        if age_above:
            filters['min_age'] = age_above.group(1)
        elif age_below:
            filters['max_age'] = age_below.group(1)
        
        # Salary patterns
        sal_above = re.search(r'salary (?:above|over|greater than) (\d+)', message_lower)
        sal_below = re.search(r'salary (?:below|under|less than) (\d+)', message_lower)
        if sal_above:
            filters['min_salary'] = sal_above.group(1)
        elif sal_below:
            filters['max_salary'] = sal_below.group(1)
        
        # Department/Role patterns
        if 'engineering' in message_lower:
            filters['department'] = 'Engineering'
        elif 'sales' in message_lower:
            filters['department'] = 'Sales'
        elif 'hr' in message_lower:
            filters['department'] = 'HR'
        
        if 'manager' in message_lower:
            filters['role'] = 'Manager'
        elif 'developer' in message_lower:
            filters['role'] = 'Developer'
        
        # If we found any filters, use list_people
        if filters:
            return await mcp_client.call_tool('list_people', filters)
        
        # Name search patterns
        name_patterns = ['find', 'search', 'who is', 'show me']
        for pattern in name_patterns:
            if pattern in message_lower:
                name = message_lower.replace(pattern, '').strip()
                if name:
                    return await mcp_client.call_tool('get_person_fuzzy', {'name': name})
        
        # Simple name search (if no special keywords)
        words = message_lower.split()
        if len(words) <= 3 and not any(w in ['hello', 'hi', 'help', 'what', 'how'] for w in words):
            return await mcp_client.call_tool('get_person_fuzzy', {'name': message})
        
        return "Try: 'find john', 'age above 30', 'salary below 50000', 'engineering managers'"
#!/usr/bin/env python3
"""MCP Server for People Directory"""

import asyncio
import json
from datetime import datetime
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
)

from .csv_data import get_people_data
from .fuzzy import fuzzy_search_people

# Initialize server
server = Server("people-directory")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="ping",
            description="Health check - returns pong with timestamp",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_person_exact",
            description="Find people with exact name match (case-insensitive)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name to search for"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="get_person_fuzzy",
            description="Find people with fuzzy/typo-tolerant name search",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name to search for (may contain typos)"
                    },
                    "maxResults": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 3
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="list_people",
            description="List people filtered by department, role, and/or location",
            inputSchema={
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "description": "Filter by department"
                    },
                    "role": {
                        "type": "string", 
                        "description": "Filter by role"
                    },
                    "location": {
                        "type": "string",
                        "description": "Filter by location"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 20
                    }
                },
                "required": []
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> Sequence[TextContent]:
    """Handle tool calls"""
    if arguments is None:
        arguments = {}
    
    people_data = get_people_data()
    
    if name == "ping":
        timestamp = datetime.now().isoformat()
        return [TextContent(type="text", text=f"pong - {timestamp}")]
    
    elif name == "get_person_exact":
        search_name = arguments.get("name", "").lower()
        matches = []
        
        for person in people_data:
            if (person["full_name"].lower() == search_name or 
                person["preferred_name"].lower() == search_name):
                matches.append(person)
        
        if not matches:
            return [TextContent(type="text", text=f"No person found with exact name: {arguments.get('name')}")]
        
        result_text = f"Found {len(matches)} exact match(es) for '{arguments.get('name')}':\n"
        for person in matches:
            result_text += f"- {person['full_name']} ({person['preferred_name']}) - {person['role']} in {person['department']}\n"
        
        return [TextContent(type="text", text=result_text + f"\nFull data: {json.dumps(matches, indent=2)}")]
    
    elif name == "get_person_fuzzy":
        search_name = arguments.get("name", "")
        max_results = arguments.get("maxResults", 3)
        
        results = fuzzy_search_people(people_data, search_name, max_results)
        
        if not results["candidates"]:
            return [TextContent(type="text", text=f"No close matches found for: {search_name}")]
        
        best_match = results["candidates"][0]
        result_text = f"Fuzzy search for '{search_name}':\n"
        result_text += f"Best match: {best_match['matched_name']} (similarity: {best_match['similarity']:.2f})\n\n"
        
        if best_match["similarity"] > 0.85:
            result_text += "High confidence match - likely the intended person.\n\n"
        elif best_match["similarity"] < 0.6:
            result_text += "Low confidence - no close match found.\n\n"
        
        result_text += "All candidates:\n"
        for candidate in results["candidates"]:
            person = candidate["person"]
            result_text += f"- {candidate['matched_name']} (similarity: {candidate['similarity']:.2f}) - {person['role']} in {person['department']}\n"
        
        return [TextContent(type="text", text=result_text + f"\nFull data: {json.dumps(results, indent=2)}")]
    
    elif name == "list_people":
        department = arguments.get("department")
        role = arguments.get("role") 
        location = arguments.get("location")
        limit = arguments.get("limit", 20)
        
        filtered_people = people_data.copy()
        
        if department:
            filtered_people = [p for p in filtered_people if p["department"].lower() == department.lower()]
        if role:
            filtered_people = [p for p in filtered_people if p["role"].lower() == role.lower()]
        if location:
            filtered_people = [p for p in filtered_people if p["location"].lower() == location.lower()]
        
        filtered_people = filtered_people[:limit]
        
        filters_used = []
        if department: filters_used.append(f"department='{department}'")
        if role: filters_used.append(f"role='{role}'")
        if location: filters_used.append(f"location='{location}'")
        
        filter_text = f" with filters: {', '.join(filters_used)}" if filters_used else ""
        result_text = f"Found {len(filtered_people)} people{filter_text}:\n"
        
        for person in filtered_people:
            result_text += f"- {person['full_name']} - {person['role']} in {person['department']} ({person['location']})\n"
        
        return [TextContent(type="text", text=result_text + f"\nFull data: {json.dumps(filtered_people, indent=2)}")]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point for the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Enhanced MCP Server with Mem0 for Managing Coding Preferences.
This server includes CORS support and additional endpoints for n8n integration.
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

import aiohttp
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="MCP Server with Mem0")

# Add CORS middleware with enhanced configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,  # 24 hours in seconds
)

# API Key validation
MEM0_API_KEY = os.getenv("MEM0_API_KEY")
if not MEM0_API_KEY:
    logger.error("MEM0_API_KEY environment variable is not set")
    sys.exit(1)

# Mem0 API URL
MEM0_API_URL = "https://api.mem0.ai"


class CodingPreference(BaseModel):
    """Model for a coding preference."""
    title: str
    content: str
    language: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class FunctionArguments(BaseModel):
    """Model for function arguments in tool calls."""
    text: Optional[str] = None
    query: Optional[str] = None


class Function(BaseModel):
    """Model for function in tool calls."""
    name: str
    arguments: Union[Dict[str, Any], FunctionArguments]


class ToolCall(BaseModel):
    """Model for tool call requests."""
    id: str
    function: Function


class MessageRequest(BaseModel):
    """Model for message requests."""
    type: str = Field(..., description="The type of message, e.g., 'tool_call'")
    tool_call: Optional[ToolCall] = Field(None, description="The tool call details if type is 'tool_call'")


@dataclass
class MCPMessage:
    """A message in the Model Context Protocol format."""
    type: str
    content: Dict[str, Any]

    def to_json(self) -> str:
        """Convert the message to a JSON string."""
        return json.dumps({"type": self.type, "content": self.content})


@dataclass
class MCPTool:
    """A tool in the Model Context Protocol format."""
    name: str
    description: str
    input_schema: Dict[str, Any]


# Define MCP tools
MCP_TOOLS = [
    MCPTool(
        name="add_coding_preference",
        description="Add a new coding preference with code example and context",
        input_schema={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the coding preference"
                },
                "content": {
                    "type": "string",
                    "description": "Content of the coding preference (code snippet)"
                },
                "language": {
                    "type": "string",
                    "description": "Programming language of the code snippet"
                },
                "description": {
                    "type": "string",
                    "description": "Description of the coding preference"
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of tags for categorizing the preference"
                },
            },
            "required": ["title", "content", "language"]
        },
    ),
    MCPTool(
        name="get_all_coding_preferences",
        description="Get all coding preferences",
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        },
    ),
    MCPTool(
        name="search_coding_preferences",
        description="Search for coding preferences by query",
        input_schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for coding preferences"
                }
            },
            "required": ["query"]
        },
    ),
]


async def add_coding_preference(preference: Dict[str, Any]) -> Dict[str, Any]:
    """Add a new coding preference to Mem0."""
    try:
        # Handle both formats - n8n tool_call format and direct MCP format
        content = preference.get("text", preference.get("content", ""))
        title = preference.get("title", "Code Snippet")
        language = preference.get("language", "javascript")  # Default to JavaScript if not specified
        description = preference.get("description", "")
        tags = preference.get("tags", [])

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{MEM0_API_URL}/api/v1/mems",
                headers={"Authorization": f"Bearer {MEM0_API_KEY}"},
                json={
                    "content": f"# {title}\n\n"
                    f"```{language}\n{content}\n```\n\n"
                    f"{description}",
                    "tags": tags,
                },
            ) as response:
                if response.status != 200:
                    logger.error(f"Failed to add coding preference: {await response.text()}")
                    return {"success": False, "error": await response.text()}

                result = await response.json()
                return {"success": True, "id": result.get("id")}
    except Exception as e:
        logger.exception("Error adding coding preference")
        return {"success": False, "error": str(e)}


async def get_all_coding_preferences() -> Dict[str, Any]:
    """Get all coding preferences from Mem0."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{MEM0_API_URL}/api/v1/mems",
                headers={"Authorization": f"Bearer {MEM0_API_KEY}"},
            ) as response:
                if response.status != 200:
                    logger.error(f"Failed to get coding preferences: {await response.text()}")
                    return {"success": False, "error": await response.text()}

                result = await response.json()
                preferences = result.get("mems", [])
                return {"success": True, "preferences": preferences}
    except Exception as e:
        logger.exception("Error getting coding preferences")
        return {"success": False, "error": str(e)}


async def search_coding_preferences(query: str) -> Dict[str, Any]:
    """Search for coding preferences in Mem0."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{MEM0_API_URL}/api/v1/mems/search",
                headers={"Authorization": f"Bearer {MEM0_API_KEY}"},
                params={"query": query},
            ) as response:
                if response.status != 200:
                    logger.error(f"Failed to search coding preferences: {await response.text()}")
                    return {"success": False, "error": await response.text()}

                result = await response.json()
                preferences = result.get("mems", [])
                return {"success": True, "preferences": preferences}
    except Exception as e:
        logger.exception("Error searching coding preferences")
        return {"success": False, "error": str(e)}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/sse")
async def sse_endpoint(request: Request):
    """SSE endpoint for MCP clients to connect to."""
    async def event_generator():
        """Generate SSE events."""
        # Send initialization message
        yield f"data: {MCPMessage('server.info', {'name': 'mem0-mcp'}).to_json()}\n\n"

        # Send tool definitions
        for tool in MCP_TOOLS:
            yield f"data: {MCPMessage('server.tool', {
                'name': tool.name,
                'description': tool.description,
                'input_schema': tool.input_schema
            }).to_json()}\n\n"

        # Wait for request to disconnect
        disconnected = await request.is_disconnected()
        while not disconnected:
            await asyncio.sleep(1)
            disconnected = await request.is_disconnected()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@app.post("/mcp")
async def mcp_endpoint(request: Request) -> JSONResponse:
    """Endpoint for handling MCP tool calls."""
    try:
        data = await request.json()
        tool_name = data.get("name")
        arguments = data.get("arguments", {})

        if tool_name == "add_coding_preference":
            result = await add_coding_preference(arguments)
            return JSONResponse(result)

        elif tool_name == "get_all_coding_preferences":
            result = await get_all_coding_preferences()
            return JSONResponse(result)

        elif tool_name == "search_coding_preferences":
            result = await search_coding_preferences(arguments["query"])
            return JSONResponse(result)

        else:
            return JSONResponse(
                {"error": f"Unknown tool: {tool_name}"},
                status_code=400
            )

    except Exception as e:
        logger.exception("Error processing MCP request")
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )


@app.post("/messages/")
async def messages_endpoint(message: MessageRequest) -> JSONResponse:
    """Enhanced endpoint for handling n8n tool calls."""
    try:
        logger.info(f"Received message of type: {message.type}")

        if message.type == "tool_call" and message.tool_call:
            tool_name = message.tool_call.function.name
            arguments = message.tool_call.function.arguments

            if isinstance(arguments, dict):
                # No validation needed, just use the dict
                pass
            else:
                # Convert Pydantic model to dict
                arguments = arguments.dict(exclude_unset=True)

            logger.info(f"Processing tool call: {tool_name} with arguments: {arguments}")

            if tool_name == "add_coding_preference":
                result = await add_coding_preference(arguments)
                return JSONResponse(result)

            elif tool_name == "get_all_coding_preferences":
                result = await get_all_coding_preferences()
                return JSONResponse(result)

            elif tool_name == "search_coding_preferences":
                query = arguments.get("query", "")
                result = await search_coding_preferences(query)
                return JSONResponse(result)

            else:
                return JSONResponse(
                    {"error": f"Unknown tool: {tool_name}"},
                    status_code=400
                )

        return JSONResponse(
            {"error": "Invalid message format"},
            status_code=400
        )

    except Exception as e:
        logger.exception("Error processing message")
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="MCP Server with Mem0 for Managing Coding Preferences"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("HOST", "0.0.0.0"),
        help="Host to bind the server to"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", 8080)),
        help="Port to bind the server to"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    logger.info(f"Starting server with CORS support on {args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)

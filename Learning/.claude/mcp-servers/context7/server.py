#!/usr/bin/env python3
"""
Context7 MCP Server
Provides contextual information and tools through the Model Context Protocol
"""

import asyncio
import json
import sys
import os
from typing import Dict, Any, List

# Simple in-memory storage for demonstration
context7_storage = {}

async def handle_request(reader, writer):
    """Handle incoming MCP requests"""
    try:
        # Read the request line
        line = await reader.readline()
        request_line = line.decode().strip()

        # Parse headers
        headers = {}
        while True:
            line = await reader.readline()
            line_str = line.decode().strip()
            if not line_str:
                break
            key, value = line_str.split(":", 1)
            headers[key.strip()] = value.strip()

        # Read the content length
        content_length = int(headers.get("Content-Length", 0))

        # Read the body
        body = await reader.read(content_length)
        request = json.loads(body.decode())

        # Process the request based on method
        method = request.get("method")

        if method == "tools/list":
            response = list_tools()
        elif method.startswith("tools/execute/"):
            tool_name = method.split("tools/execute/", 1)[1]
            response = await execute_tool(tool_name, request.get("params", {}))
        elif method == "initialize":
            response = initialize()
        else:
            response = {
                "error": {
                    "code": -32601,
                    "message": f"Method {method} not supported"
                }
            }

        # Send response
        response_body = json.dumps(response)
        response_headers = f"Content-Length: {len(response_body)}\r\n\r\n"
        writer.write(response_headers.encode() + response_body.encode())
        await writer.drain()

    except Exception as e:
        error_response = {
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }
        response_body = json.dumps(error_response)
        response_headers = f"Content-Length: {len(response_body)}\r\n\r\n"
        writer.write(response_headers.encode() + response_body.encode())
        await writer.drain()

def list_tools():
    """List available tools"""
    return {
        "result": {
            "tools": [
                {
                    "name": "context7_query",
                    "description": "Query the Context7 system for information",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The query to send to Context7"
                            }
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "context7_store",
                    "description": "Store information in the Context7 system",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "key": {
                                "type": "string",
                                "description": "The key to store the information under"
                            },
                            "value": {
                                "type": "string",
                                "description": "The value to store"
                            }
                        },
                        "required": ["key", "value"]
                    }
                }
            ]
        }
    }

async def execute_tool(tool_name: str, params: Dict[str, Any]):
    """Execute a specific tool"""
    global context7_storage

    if tool_name == "context7_query":
        query = params.get("query", "")
        # In a real implementation, this would query your Context7 system
        result = f"Query result for: {query}"
        if query in context7_storage:
            result = context7_storage[query]

        return {
            "result": {
                "output": result
            }
        }

    elif tool_name == "context7_store":
        key = params.get("key", "")
        value = params.get("value", "")
        context7_storage[key] = value

        return {
            "result": {
                "message": f"Stored key '{key}' with value of length {len(value)}"
            }
        }

    else:
        return {
            "error": {
                "code": -32601,
                "message": f"Tool {tool_name} not found"
            }
        }

def initialize():
    """Initialize the server"""
    return {
        "result": {
            "protocolVersion": "1.0",
            "serverInfo": {
                "name": "context7-mcp-server",
                "version": "1.0.0"
            }
        }
    }

async def main():
    """Main server function"""
    server = await asyncio.start_server(handle_request, '127.0.0.1', 0)

    # Print the port to stdout so Claude can connect to it
    port = server.sockets[0].getsockname()[1]
    print(f"Context7 MCP Server listening on port {port}", file=sys.stderr)
    sys.stderr.flush()

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
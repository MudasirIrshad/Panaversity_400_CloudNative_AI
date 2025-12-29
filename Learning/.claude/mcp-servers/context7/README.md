# Context7 MCP Server

This is an MCP (Model Context Protocol) server that provides integration with the Context7 system.

## Features

- `context7_query`: Query the Context7 system for information
- `context7_store`: Store information in the Context7 system

## Configuration

The server is configured in `.claude/settings.json` and will be automatically loaded by Claude Code.

## Usage

Once configured, you can ask Claude to use the Context7 tools by mentioning them in your prompts. Claude will automatically discover and use the available tools.

## Implementation

The server is implemented in Python and can be found at:
`.claude/mcp-servers/context7/server.py`

You can customize the implementation to connect to your actual Context7 system by modifying the `execute_tool` function in the server implementation.
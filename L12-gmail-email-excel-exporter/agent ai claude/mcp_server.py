"""
MCP Server for Gmail Email Management

This module implements an MCP (Model Context Protocol) server that exposes
Gmail email fetching and Excel export functionality as tools for Claude.
"""

import asyncio
import json
import os
from typing import Any, List, Dict

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from gmail_auth import GmailAuthenticator
from email_fetcher import EmailFetcher
from excel_handler import ExcelHandler


# Global instances
authenticator = GmailAuthenticator()
gmail_service = None
email_fetcher = None


def initialize_gmail():
    """Initialize Gmail service if not already initialized."""
    global gmail_service, email_fetcher

    if gmail_service is None:
        gmail_service = authenticator.get_gmail_service()
        email_fetcher = EmailFetcher(gmail_service)


# Create MCP server instance
server = Server("mem-gmail-server")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    List available tools for Claude.

    Returns:
        List of tool definitions
    """
    return [
        Tool(
            name="fetch_gmail_emails",
            description="Fetch emails from Gmail using a search query. Supports full Gmail search syntax including filters like 'from:', 'subject:', 'after:', 'is:unread', etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Gmail search query (e.g., 'from:example@gmail.com', 'subject:invoice after:2024/01/01', 'is:unread')",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of emails to fetch (default: 100)",
                        "default": 100,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="export_emails_to_excel",
            description="Export a list of emails to an Excel file. Takes email data and creates a formatted spreadsheet.",
            inputSchema={
                "type": "object",
                "properties": {
                    "emails": {
                        "type": "array",
                        "description": "Array of email objects to export (typically from fetch_gmail_emails)",
                        "items": {
                            "type": "object"
                        }
                    },
                    "filename": {
                        "type": "string",
                        "description": "Output filename (e.g., 'invoices.xlsx'). If not provided, auto-generated with timestamp.",
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Output directory path (default: current directory)",
                        "default": ".",
                    },
                    "full_body": {
                        "type": "boolean",
                        "description": "Include full email body without truncation (default: false)",
                        "default": False,
                    },
                },
                "required": ["emails"],
            },
        ),
        Tool(
            name="get_email_details",
            description="Get full details of a specific email by its message ID. Returns complete email data including full body content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "message_id": {
                        "type": "string",
                        "description": "Gmail message ID",
                    },
                },
                "required": ["message_id"],
            },
        ),
        Tool(
            name="search_and_export",
            description="Combined operation: search for emails and immediately export them to Excel. Convenience tool for one-step operations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Gmail search query",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of emails to fetch (default: 100)",
                        "default": 100,
                    },
                    "filename": {
                        "type": "string",
                        "description": "Output filename (optional)",
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Output directory path (default: current directory)",
                        "default": ".",
                    },
                    "full_body": {
                        "type": "boolean",
                        "description": "Include full email body (default: false)",
                        "default": False,
                    },
                },
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool execution requests.

    Args:
        name: Tool name to execute
        arguments: Tool arguments

    Returns:
        List of text content with results
    """
    try:
        # Initialize Gmail service
        initialize_gmail()

        if name == "fetch_gmail_emails":
            return await fetch_gmail_emails_tool(arguments)

        elif name == "export_emails_to_excel":
            return await export_emails_to_excel_tool(arguments)

        elif name == "get_email_details":
            return await get_email_details_tool(arguments)

        elif name == "search_and_export":
            return await search_and_export_tool(arguments)

        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error executing tool '{name}': {str(e)}"
        )]


async def fetch_gmail_emails_tool(arguments: dict) -> list[TextContent]:
    """
    Fetch emails from Gmail.

    Args:
        arguments: Tool arguments with 'query' and optional 'max_results'

    Returns:
        List of text content with email data
    """
    query = arguments.get("query")
    max_results = arguments.get("max_results", 100)

    if not query:
        return [TextContent(
            type="text",
            text="Error: 'query' parameter is required"
        )]

    # Fetch emails
    emails = email_fetcher.search_emails(query, max_results)

    # Format response
    result = {
        "success": True,
        "count": len(emails),
        "query": query,
        "emails": emails
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def export_emails_to_excel_tool(arguments: dict) -> list[TextContent]:
    """
    Export emails to Excel.

    Args:
        arguments: Tool arguments with 'emails' and optional filename/output_dir

    Returns:
        List of text content with export result
    """
    emails = arguments.get("emails", [])
    filename = arguments.get("filename")
    output_dir = arguments.get("output_dir", ".")
    full_body = arguments.get("full_body", False)

    if not emails:
        return [TextContent(
            type="text",
            text="Error: 'emails' parameter is required and must not be empty"
        )]

    # Export to Excel
    handler = ExcelHandler()

    if full_body:
        output_path = handler.export_emails_with_full_body(
            emails,
            filename=filename,
            output_dir=output_dir
        )
    else:
        output_path = handler.export_emails(
            emails,
            filename=filename,
            output_dir=output_dir
        )

    result = {
        "success": True,
        "count": len(emails),
        "output_path": output_path,
        "full_body": full_body
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def get_email_details_tool(arguments: dict) -> list[TextContent]:
    """
    Get details of specific email.

    Args:
        arguments: Tool arguments with 'message_id'

    Returns:
        List of text content with email details
    """
    message_id = arguments.get("message_id")

    if not message_id:
        return [TextContent(
            type="text",
            text="Error: 'message_id' parameter is required"
        )]

    # Get email details
    email = email_fetcher.get_email_details(message_id)

    if not email:
        return [TextContent(
            type="text",
            text=f"Error: Email with ID '{message_id}' not found"
        )]

    result = {
        "success": True,
        "email": email
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def search_and_export_tool(arguments: dict) -> list[TextContent]:
    """
    Combined search and export operation.

    Args:
        arguments: Tool arguments with query and export parameters

    Returns:
        List of text content with operation result
    """
    query = arguments.get("query")
    max_results = arguments.get("max_results", 100)
    filename = arguments.get("filename")
    output_dir = arguments.get("output_dir", ".")
    full_body = arguments.get("full_body", False)

    if not query:
        return [TextContent(
            type="text",
            text="Error: 'query' parameter is required"
        )]

    # Fetch emails
    emails = email_fetcher.search_emails(query, max_results)

    if not emails:
        return [TextContent(
            type="text",
            text=f"No emails found for query: '{query}'"
        )]

    # Export to Excel
    handler = ExcelHandler()

    if full_body:
        output_path = handler.export_emails_with_full_body(
            emails,
            filename=filename,
            output_dir=output_dir
        )
    else:
        output_path = handler.export_emails(
            emails,
            filename=filename,
            output_dir=output_dir
        )

    result = {
        "success": True,
        "query": query,
        "emails_found": len(emails),
        "output_path": output_path,
        "full_body": full_body
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]


async def main():
    """Main entry point for MCP server."""
    # Run the server using stdin/stdout streams
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mem-gmail-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())

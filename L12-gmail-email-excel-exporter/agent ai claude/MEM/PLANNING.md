# MEM Project Planning

## Overview
MEM (Mail Excel Manager) is a Python-based system that connects to Gmail via OAuth2, fetches specific emails, and exports them to Excel format. It includes MCP (Model Context Protocol) server integration for Claude agent interaction.

## Architecture

### Components

#### 1. Gmail OAuth Handler (`gmail_auth.py`)
- Manages OAuth2 authentication flow
- Stores and refreshes tokens
- Provides authenticated Gmail API client

#### 2. Email Fetcher (`email_fetcher.py`)
- Searches and retrieves emails based on criteria
- Parses email metadata and content
- Extracts relevant fields (sender, subject, date, body, attachments)

#### 3. Excel Exporter (`excel_handler.py`)
- Formats email data for Excel output
- Creates structured spreadsheets with proper columns
- Handles multiple emails in batch

#### 4. MCP Server Tool (`mcp_server.py`)
- Implements Google MCP Server SDK
- Exposes tools for Claude agent to call
- Provides interface for fetching and exporting emails

#### 5. Main Application (`main.py`)
- CLI interface for standalone usage
- Orchestrates all components
- Configuration management

### Data Flow

```
User/Claude Agent
    |
    v
MCP Server Tool (optional entry point)
    |
    v
Main Application
    |
    +---> Gmail OAuth Handler ---> Gmail API
    |
    +---> Email Fetcher ---> Parse Emails
    |
    +---> Excel Exporter ---> Save to .xlsx file
```

## Technology Stack

- **Python 3.8+**: Core language
- **google-auth-oauthlib**: OAuth2 authentication
- **google-api-python-client**: Gmail API interaction
- **openpyxl**: Excel file creation
- **mcp**: Model Context Protocol SDK
- **python-dotenv**: Environment configuration

## Security Considerations

- Store credentials in `.env` file (not version controlled)
- Use OAuth2 for secure authentication
- Store tokens in local `token.json` file
- Implement proper error handling for API failures
- Follow Gmail API rate limits and quotas

## Configuration

- Gmail API credentials (OAuth2 client ID and secret)
- Email search query parameters
- Output file naming conventions
- MCP server port and settings

## Future Enhancements

- Support for multiple Gmail accounts
- Advanced email filtering options
- Attachment downloading
- Email content analysis
- Scheduled fetching with cron jobs
- Database storage for email metadata

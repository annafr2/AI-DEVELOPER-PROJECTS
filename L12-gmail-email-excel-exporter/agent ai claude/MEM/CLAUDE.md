# Claude Integration Guide

## Overview

This document explains how to integrate the MEM (Mail Excel Manager) system with Claude using the Model Context Protocol (MCP). The MCP server allows Claude to interact with Gmail and export emails to Excel through natural language commands.

## Architecture

```
Claude CLI (claude-cli)
    |
    | MCP Protocol
    v
MEM MCP Server (mcp_server.py)
    |
    +---> Gmail OAuth Handler
    |
    +---> Email Fetcher
    |
    +---> Excel Exporter
```

## MCP Server Setup

### 1. Install MCP SDK

The MCP server uses the official Python MCP SDK:

```bash
pip install mcp
```

### 2. Start the MCP Server

```bash
python mcp_server.py
```

The server will start and listen for connections from Claude CLI.

### 3. Configure Claude CLI

Add the MEM MCP server to your Claude CLI configuration:

```json
{
  "mcpServers": {
    "mem-gmail": {
      "command": "python",
      "args": ["/absolute/path/to/MEM/mcp_server.py"],
      "env": {
        "GMAIL_CREDENTIALS_PATH": "/path/to/credentials.json"
      }
    }
  }
}
```

Configuration file location:
- macOS/Linux: `~/.config/claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

## Available Tools

The MCP server exposes three main tools to Claude:

### 1. fetch_gmail_emails

Fetches emails from Gmail based on a search query.

**Parameters:**
- `query` (string, required): Gmail search query (e.g., "from:example@gmail.com", "subject:invoice")
- `max_results` (integer, optional): Maximum number of emails to fetch (default: 100)

**Example usage in Claude:**
```
Claude, fetch my emails from GitHub sent in the last week
```

**Behind the scenes:**
```json
{
  "tool": "fetch_gmail_emails",
  "arguments": {
    "query": "from:noreply@github.com newer_than:7d",
    "max_results": 50
  }
}
```

### 2. export_emails_to_excel

Exports fetched emails to an Excel file.

**Parameters:**
- `emails` (array, required): List of email objects to export
- `filename` (string, optional): Output filename (default: "emails_YYYYMMDD_HHMMSS.xlsx")
- `output_dir` (string, optional): Output directory (default: current directory)

**Example usage in Claude:**
```
Export those emails to an Excel file named "github_notifications.xlsx"
```

**Behind the scenes:**
```json
{
  "tool": "export_emails_to_excel",
  "arguments": {
    "emails": [...],
    "filename": "github_notifications.xlsx"
  }
}
```

### 3. get_email_details

Retrieves full details of a specific email by its message ID.

**Parameters:**
- `message_id` (string, required): Gmail message ID

**Example usage in Claude:**
```
Show me the full content of the first email
```

## Usage Examples

### Example 1: Fetch and Export Recent Invoices

**User:** "Claude, fetch all invoice emails from the last 3 months and save them to Excel"

**Claude's actions:**
1. Calls `fetch_gmail_emails` with query: "subject:invoice after:2024/07/01"
2. Calls `export_emails_to_excel` with the results
3. Returns: "I've fetched 15 invoice emails and saved them to `emails_20241025_143022.xlsx`"

### Example 2: Search Specific Sender

**User:** "Get all unread emails from support@company.com"

**Claude's actions:**
1. Calls `fetch_gmail_emails` with query: "from:support@company.com is:unread"
2. Returns: Summary of found emails with option to export

### Example 3: Complex Query

**User:** "Find emails with attachments from billing@stripe.com in the last 30 days and export them"

**Claude's actions:**
1. Calls `fetch_gmail_emails` with query: "from:billing@stripe.com has:attachment newer_than:30d"
2. Calls `export_emails_to_excel`
3. Returns: Confirmation with file path

## Gmail Search Query Syntax

The MCP server supports full Gmail search syntax:

### Basic Queries
- `from:sender@example.com` - Emails from specific sender
- `to:recipient@example.com` - Emails to specific recipient
- `subject:keyword` - Emails with keyword in subject
- `keyword` - General keyword search

### Date Filters
- `after:2024/01/01` - After specific date
- `before:2024/12/31` - Before specific date
- `newer_than:7d` - Newer than 7 days
- `older_than:1m` - Older than 1 month

### Status Filters
- `is:unread` - Unread emails
- `is:read` - Read emails
- `is:starred` - Starred emails
- `is:important` - Important emails

### Attachment Filters
- `has:attachment` - Has any attachment
- `filename:pdf` - Has PDF attachment
- `filename:invoice.pdf` - Specific filename

### Label Filters
- `label:work` - Emails with "work" label
- `label:important` - Important label

### Combining Queries
Use spaces for AND, OR for alternatives:
- `from:example.com subject:invoice` - From example.com AND contains invoice
- `from:gmail.com OR from:google.com` - From either domain

## Error Handling

The MCP server provides clear error messages:

### Authentication Errors
```
Error: Gmail authentication failed. Please run: python main.py --auth
```

### Invalid Query Errors
```
Error: Invalid Gmail query syntax. Please check your search terms.
```

### Rate Limit Errors
```
Error: Gmail API rate limit exceeded. Please try again in a few minutes.
```

### Export Errors
```
Error: Failed to create Excel file. Check write permissions for output directory.
```

## Debugging

### Enable Verbose Logging

Set environment variable:
```bash
export MEM_DEBUG=1
python mcp_server.py
```

### View Server Logs

Logs are written to `mcp_server.log` in the project directory.

### Test MCP Server Manually

Use the MCP inspector tool:
```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```

## Security Considerations

1. **OAuth Tokens**: Tokens are stored in `token.json` - keep this file secure
2. **Credentials**: Never commit `credentials.json` to version control
3. **File Permissions**: Ensure proper permissions on sensitive files
4. **API Quotas**: Be aware of Gmail API rate limits (1 billion quota units/day)
5. **Data Privacy**: Exported Excel files contain email content - handle appropriately

## Troubleshooting

### Claude Can't Find MCP Server

1. Check Claude CLI configuration file path
2. Verify absolute path to `mcp_server.py` in config
3. Ensure Python executable is in PATH
4. Check server logs for startup errors

### Authentication Issues

1. Run standalone authentication: `python main.py --auth`
2. Verify `credentials.json` is valid
3. Check token.json permissions
4. Re-authorize if token expired

### No Emails Found

1. Test query directly in Gmail web interface
2. Check Gmail API is enabled in Google Cloud Console
3. Verify account has emails matching query
4. Check for typos in query syntax

### Excel Export Fails

1. Verify write permissions in output directory
2. Check disk space
3. Ensure openpyxl is installed
4. Try different output path

## Advanced Usage

### Custom MCP Server Configuration

Edit `mcp_server.py` to customize:

```python
# Change default max results
DEFAULT_MAX_RESULTS = 200

# Change default output directory
DEFAULT_OUTPUT_DIR = "/path/to/exports"

# Add custom tool
@server.tool()
async def custom_email_filter(emails: list, keyword: str):
    # Custom filtering logic
    pass
```

### Extending Tools

Add new tools by decorating functions with `@server.tool()`:

```python
@server.tool()
async def search_and_export(query: str, filename: str):
    """Combined search and export operation"""
    emails = await fetch_gmail_emails(query)
    result = await export_emails_to_excel(emails, filename)
    return result
```

## Performance Tips

1. **Limit Results**: Use `max_results` to avoid fetching too many emails
2. **Specific Queries**: More specific queries are faster
3. **Caching**: Consider implementing caching for repeated queries
4. **Batch Operations**: Export multiple queries to same file
5. **Background Processing**: For large exports, consider async processing

## Integration with Other Tools

### Export to Google Sheets

Modify `excel_handler.py` to support Google Sheets API

### Email to Database

Add database storage tool to MCP server

### Scheduled Exports

Use cron/scheduler to run periodic exports

### Email Notifications

Add tool to send email summaries

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Claude CLI Documentation](https://docs.anthropic.com/claude/docs)
- [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk)

## Support

For issues or questions:
1. Check TASKS.md for implementation status
2. Review TEST.md for testing guidance
3. Check server logs for errors
4. Refer to PLANNING.md for architecture details

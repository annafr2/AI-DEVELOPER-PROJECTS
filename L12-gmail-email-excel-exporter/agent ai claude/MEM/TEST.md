# MEM Project Test Plan

## Unit Tests

### gmail_auth.py Tests
```
test_oauth_flow_initialization()
  - Verify credentials file is loaded correctly
  - Check OAuth flow is created with proper scopes

test_token_storage()
  - Test token.json creation
  - Verify token persistence
  - Test token loading from file

test_token_refresh()
  - Mock expired token
  - Verify refresh mechanism works
  - Check new token is saved

test_authentication_errors()
  - Test missing credentials file
  - Test invalid credentials
  - Test network failures
```

### email_fetcher.py Tests
```
test_email_search()
  - Test basic query execution
  - Verify correct API calls
  - Check result parsing

test_email_parsing()
  - Test metadata extraction
  - Verify body content parsing
  - Test HTML to text conversion

test_pagination()
  - Mock large result set
  - Verify all pages are fetched
  - Test page token handling

test_filter_combinations()
  - Test date range filters
  - Test label filters
  - Test keyword searches

test_error_handling()
  - Test API quota exceeded
  - Test network timeouts
  - Test malformed responses
```

### excel_handler.py Tests
```
test_excel_creation()
  - Verify file is created
  - Check column headers
  - Test basic data writing

test_data_formatting()
  - Test date formatting
  - Test text wrapping
  - Test cell styling

test_special_characters()
  - Test Unicode characters
  - Test emojis in emails
  - Test special symbols

test_large_datasets()
  - Test with 1000+ emails
  - Verify performance
  - Check memory usage
```

### mcp_server.py Tests
```
test_tool_registration()
  - Verify all tools are registered
  - Check tool schemas
  - Test tool discovery

test_tool_execution()
  - Test fetch_gmail_emails tool
  - Test export_emails_to_excel tool
  - Test get_email_details tool

test_error_responses()
  - Test invalid parameters
  - Test authentication failures
  - Test proper error formatting
```

## Integration Tests

### End-to-End Flow
```
test_full_workflow()
  1. Authenticate with Gmail
  2. Fetch emails with query
  3. Export to Excel
  4. Verify Excel contents

test_mcp_server_integration()
  1. Start MCP server
  2. Send tool request via Claude CLI
  3. Verify response format
  4. Check generated Excel file
```

### Real Gmail API Tests
```
test_real_authentication()
  - Use test Gmail account
  - Complete OAuth flow
  - Verify access token

test_real_email_fetch()
  - Fetch from test account
  - Verify real email data
  - Test various query types
```

## Manual Testing Checklist

### Setup Tests
- [ ] Fresh installation in new environment
- [ ] Dependency installation completes
- [ ] Configuration file creation works
- [ ] Gmail API credentials setup

### Authentication Tests
- [ ] First-time OAuth flow
- [ ] Browser authorization page opens
- [ ] Token is saved correctly
- [ ] Subsequent runs use cached token
- [ ] Token refresh on expiry

### Email Fetching Tests
- [ ] Simple query (e.g., "from:gmail.com")
- [ ] Date range query
- [ ] Label-based query
- [ ] Complex query with multiple criteria
- [ ] Empty result set
- [ ] Large result set (100+ emails)

### Excel Export Tests
- [ ] Single email export
- [ ] Multiple emails export
- [ ] Export with special characters
- [ ] Export with long email bodies
- [ ] File naming conventions
- [ ] Open file in Excel/LibreOffice

### MCP Server Tests
- [ ] Server starts without errors
- [ ] Claude CLI can connect
- [ ] Tools are discoverable
- [ ] Each tool executes successfully
- [ ] Error messages are clear
- [ ] Server handles concurrent requests

### Error Scenarios
- [ ] Invalid Gmail credentials
- [ ] Network disconnection during fetch
- [ ] Disk full during export
- [ ] Invalid query syntax
- [ ] Permission denied errors
- [ ] Rate limit exceeded

### Cross-Platform Tests
- [ ] Windows compatibility
- [ ] macOS compatibility
- [ ] Linux compatibility
- [ ] WSL compatibility

## Performance Tests

### Benchmarks
```
Small dataset: 10 emails
  - Fetch time: < 5 seconds
  - Export time: < 1 second

Medium dataset: 100 emails
  - Fetch time: < 30 seconds
  - Export time: < 5 seconds

Large dataset: 1000 emails
  - Fetch time: < 5 minutes
  - Export time: < 30 seconds
```

### Memory Usage
- Monitor memory during large fetches
- Check for memory leaks in long-running MCP server
- Verify cleanup after operations

## Security Tests

- [ ] Credentials are not logged
- [ ] Tokens are stored securely
- [ ] No sensitive data in error messages
- [ ] `.env` file is not committed to git
- [ ] Credentials file permissions are correct

## Test Data

### Sample Test Queries
```
"from:noreply@github.com"
"subject:invoice after:2024/01/01"
"is:unread label:important"
"has:attachment filename:pdf"
"newer_than:7d from:billing@stripe.com"
```

### Expected Output Format
```
Excel columns:
- Date
- From
- To
- Subject
- Body Preview
- Labels
- Has Attachment
- Message ID
```

## Automated Testing

Run all tests:
```bash
pytest tests/ -v --cov=. --cov-report=html
```

Run specific test suite:
```bash
pytest tests/test_gmail_auth.py -v
pytest tests/test_email_fetcher.py -v
pytest tests/test_excel_handler.py -v
pytest tests/test_mcp_server.py -v
```

## Continuous Integration

- Set up GitHub Actions for automated testing
- Run tests on pull requests
- Test on multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)
- Generate coverage reports

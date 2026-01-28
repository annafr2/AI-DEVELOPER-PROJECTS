# Product Requirements Document (PRD)
## Gmail to Calendar Automation System

### Version: 1.0
### Date: January 2026
### Status: Development

---

## Executive Summary

An automated system that monitors Gmail inbox, identifies relevant emails based on search criteria, and automatically creates corresponding Google Calendar events. The system supports both traditional config-based search and AI-powered natural language search.

---

## Goals and Objectives

### Primary Goals
1. Automate the process of creating calendar events from emails
2. Reduce manual calendar management effort
3. Ensure important emails are converted to actionable calendar items

### Success Metrics
- Successfully process 95%+ of matching emails
- Event creation time under 5 seconds per email
- Zero duplicate events for the same email
- Minimal false positives (irrelevant emails)

---

## User Stories

### As a busy professional, I want to:
- Automatically add meeting invitations to my calendar
- Convert deadline emails into calendar reminders
- Track appointments without manual entry
- Process emails even when I'm away from computer

### As an admin, I want to:
- Configure search criteria without coding
- Choose between precise search and AI interpretation
- Control when and how often scanning occurs
- Monitor what emails are being processed

---

## Functional Requirements

### FR1: Email Scanning
- **FR1.1**: Support Gmail API search syntax
- **FR1.2**: Support natural language search via LLM
- **FR1.3**: Filter by sender, subject, labels, read/unread status
- **FR1.4**: Handle multiple matching emails in single scan
- **FR1.5**: Extract email metadata (subject, sender, body, ID)

### FR2: Calendar Integration
- **FR2.1**: Create events in Google Calendar
- **FR2.2**: Set event title from email subject
- **FR2.3**: Add email content to event description
- **FR2.4**: Link back to source email
- **FR2.5**: Extract date/time from email when possible

### FR3: Execution Modes
- **FR3.1**: Single-run mode: Execute once and exit
- **FR3.2**: Continuous mode: Scan at configurable intervals
- **FR3.3**: Graceful shutdown on user interrupt
- **FR3.4**: Prevent duplicate processing of same email

### FR4: LLM Features (Optional)
- **FR4.1**: Convert natural language to Gmail search query
- **FR4.2**: Extract event details (title, date, time, location)
- **FR4.3**: Fallback to basic behavior if LLM unavailable
- **FR4.4**: Handle LLM API errors gracefully

### FR5: Email Management
- **FR5.1**: Mark processed emails as read
- **FR5.2**: Only mark as read after successful event creation
- **FR5.3**: Leave email unread if processing fails

---

## Non-Functional Requirements

### NFR1: Security
- OAuth 2.0 authentication for Google APIs
- Secure credential storage (not in code)
- API keys in environment variables only
- No credentials in version control

### NFR2: Performance
- Process each email in under 5 seconds
- Support up to 10 emails per scan
- Minimal memory footprint (< 100MB)
- API rate limit awareness

### NFR3: Reliability
- Graceful handling of API failures
- Retry logic for transient errors
- Clear error messages for user
- No data loss on failure

### NFR4: Usability
- Simple configuration via .env file
- Clear console output showing progress
- Helpful error messages
- Single command to run

### NFR5: Maintainability
- Modular code structure
- Clear separation of concerns
- Maximum 150 lines per file
- Comprehensive comments

---

## Technical Requirements

### TR1: Technology Stack
- Python 3.8+
- Google Gmail API
- Google Calendar API
- OpenAI API (optional)
- OAuth 2.0

### TR2: Dependencies
- `google-auth-oauthlib`: Authentication
- `google-api-python-client`: Google APIs
- `openai`: LLM integration
- `python-dotenv`: Configuration
- `python-dateutil`: Date parsing

### TR3: Authentication Flow
1. Check for existing token
2. If expired, refresh token
3. If no token, initiate OAuth flow
4. Open browser for user consent
5. Save token for future use

### TR4: API Scopes Required
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/calendar`

---

## Configuration Options

### Required Configuration
- `credentials.json`: Google API credentials
- `RUN_MODE`: 'once' or 'continuous'

### Optional Configuration
- `SEARCH_MODE`: 'config' or 'llm'
- `SEARCH_QUERY`: Gmail search string (config mode)
- `LLM_SEARCH_PROMPT`: Natural language prompt (llm mode)
- `OPENAI_API_KEY`: OpenAI API key (llm mode)
- `SCAN_INTERVAL`: Seconds between scans (continuous mode)
- `CALENDAR_ID`: Target calendar (default: 'primary')

---

## System Architecture

### Components

**main.py**
- Entry point
- Configuration validation
- Mode selection and execution

**config.py**
- Load environment variables
- Validate configuration
- Provide configuration access

**auth.py**
- Google API authentication
- Token management
- Service object creation

**gmail_scanner.py**
- Execute Gmail searches
- Retrieve email content
- Mark emails as read

**calendar_manager.py**
- Create calendar events
- Format event data
- Handle calendar API errors

**llm_helper.py**
- Generate search queries from natural language
- Extract event details from email text
- Handle OpenAI API calls

### Data Flow

```
User → Config → Auth → Gmail Scan → Email Content → 
Event Creation → Mark Read → Repeat (if continuous)
```

### LLM Enhancement Flow

```
Natural Language Prompt → LLM → Gmail Query
Email Content → LLM → Event Details → Calendar Event
```

---

## Error Handling

### Authentication Errors
- Missing credentials.json → Clear error message with instructions
- Invalid token → Automatic refresh or re-auth
- Scope issues → List required scopes

### API Errors
- Rate limits → Wait and retry
- Network errors → Retry with exponential backoff
- Invalid response → Log and skip email

### Configuration Errors
- Missing required fields → List errors and exit
- Invalid values → Suggest valid options
- Missing API keys → Warning (for optional features)

---

## Testing Scenarios

### Basic Tests
1. Single email matching query
2. Multiple emails matching query
3. No emails matching query
4. Email already read
5. Invalid search query

### Mode Tests
1. Single-run mode completes
2. Continuous mode runs multiple iterations
3. Graceful shutdown on Ctrl+C

### LLM Tests
1. Natural language to query conversion
2. Event detail extraction
3. Fallback when LLM unavailable

### Edge Cases
1. Empty email body
2. Email without date information
3. Multiple events in single email
4. Very long email content

---

## Constraints and Limitations

### API Quotas
- Gmail API: 1 billion quota units/day
- Calendar API: 1,000,000 quota units/day
- Sufficient for most use cases

### LLM Costs
- OpenAI GPT-4: ~$0.03-0.06 per email
- Consider costs for continuous mode
- Budget accordingly

### Search Limitations
- Maximum 10 emails per scan (configurable)
- Gmail search syntax limitations
- LLM interpretation accuracy

### Calendar Limitations
- Cannot modify existing events
- Default event time if not extracted
- UTC timezone only (currently)

---

## Future Enhancements

### Phase 2 Features
- Support multiple calendars
- Custom event templates
- Email response automation
- Duplicate event detection
- Event reminder configuration

### Phase 3 Features
- Web dashboard for monitoring
- Event modification capability
- Multiple email account support
- Scheduling different search criteria
- Analytics and reporting

---

## Success Criteria

### MVP Completion
- ✅ Basic email scanning works
- ✅ Calendar events created successfully
- ✅ Both modes (config/llm) functional
- ✅ Both run modes work
- ✅ Emails marked as read
- ✅ Documentation complete

### Production Ready
- Handles errors gracefully
- No crashes in continuous mode
- Clear user feedback
- Easy setup process
- Secure credential handling

---

## Glossary

- **OAuth 2.0**: Authorization framework for API access
- **Gmail API**: Google's programmatic access to Gmail
- **Calendar API**: Google's programmatic access to Calendar
- **LLM**: Large Language Model (AI system)
- **Scope**: Permission level for API access
- **Query**: Search criteria for finding emails
- **Credential**: Authentication information

---

## References

- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Calendar API Documentation](https://developers.google.com/calendar/api)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OAuth 2.0 Specification](https://oauth.net/2/)

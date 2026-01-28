# Gmail to Calendar Automation

Automatically scan Gmail for specific emails and create Google Calendar events from them. Supports both config-based search and AI-powered natural language search using OpenAI.

![Calendar Event Example](calendar_screenshot.png)
*Example: Email automatically converted to calendar event*

## Features

- **Dual Search Modes**
  - **Config Mode**: Use Gmail search syntax for precise filtering
  - **LLM Mode**: Use natural language to describe what emails to find

- **Flexible Running Modes**
  - **Single Run**: Scan once and exit
  - **Continuous**: Scan every N seconds (configurable)

- **Smart Event Creation**
  - Automatically creates calendar events from emails
  - Uses LLM to extract event details (date, time, location) when available
  - Links back to original email
  - Marks processed emails as read

- **Easy Authentication**
  - Single OAuth flow for both Gmail and Calendar
  - Credentials saved for future runs

## Prerequisites

- Python 3.8 or higher
- Google account with Gmail and Calendar enabled
- Google Cloud project with APIs enabled (see Setup Guide)
- OpenAI API key (optional, for LLM features)

## Quick Start

### 1. Google Cloud Setup

Follow the **Google Cloud Setup Guide** in the documentation to:
- Create a Google Cloud project
- Enable Gmail and Calendar APIs
- Download `credentials.json`

### 2. Installation

```bash
# Clone or download the project
cd gmail_calendar_sync

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 3. Configuration

Edit `.env` file:

```env
# Required: Place credentials.json in project root

# Optional: For LLM features
OPENAI_API_KEY=your_key_here

# Choose mode
RUN_MODE=once  # or 'continuous'
SCAN_INTERVAL=10  # seconds (for continuous mode)

# Choose search type
SEARCH_MODE=config  # or 'llm'

# Config mode: Gmail search syntax
SEARCH_QUERY=is:unread subject:meeting

# LLM mode: Natural language
LLM_SEARCH_PROMPT=Find emails about appointments this week
```

### 4. First Run

```bash
python main.py
```

First run will:
1. Open browser for Google authentication
2. Request access to Gmail and Calendar
3. Save token for future runs
4. Start scanning emails

## Configuration Options

### Search Mode: Config

Use Gmail search syntax for precise control:

```env
SEARCH_MODE=config
SEARCH_QUERY=is:unread from:boss@company.com
```

**Examples:**
- `is:unread subject:meeting` - Unread emails with "meeting" in subject
- `from:calendar@company.com is:unread` - Unread from specific sender
- `label:important has:attachment` - Important emails with attachments
- `subject:(appointment OR schedule)` - Multiple keywords

### Search Mode: LLM

Use natural language (requires OpenAI API key):

```env
SEARCH_MODE=llm
OPENAI_API_KEY=sk-...
LLM_SEARCH_PROMPT=Find unread emails about meetings or appointments from my boss
```

**Benefits:**
- Natural language instead of search syntax
- LLM extracts event details (date, time, location) from email body
- Smarter event creation

### Run Modes

**Single Run:**
```env
RUN_MODE=once
```

**Continuous:**
```env
RUN_MODE=continuous
SCAN_INTERVAL=10  # seconds between scans
```

## Project Structure

```
gmail_calendar_sync/
├── main.py                 # Main application entry point
├── config.py              # Configuration management
├── auth.py                # Google API authentication
├── gmail_scanner.py       # Gmail operations
├── calendar_manager.py    # Calendar operations
├── llm_helper.py          # OpenAI LLM integration
├── requirements.txt       # Python dependencies
├── .env.example          # Configuration template
├── .gitignore            # Git ignore rules
├── credentials.json      # Google API credentials (download from Cloud Console)
└── token.pickle          # Auto-generated auth token
```

## Usage Examples

### Example 1: Simple Config Search

**Email you send:**
```
To: your.calendar.email@gmail.com
Subject: Team Meeting - AI
Body: Let's discuss the AI development course project progress.
```

**Configuration (.env):**
```env
RUN_MODE=once
SEARCH_MODE=config
SEARCH_QUERY=is:unread subject:meeting
```

**Result:**
- Finds all unread emails with "meeting" in subject
- Creates calendar event: "Team Meeting - AI"
- Default time: Tomorrow at 10 AM (if no specific time mentioned)
- Marks email as read

**What you'll see in console:**
```
--- Starting email scan ---
Found 1 email(s)

Processing email: abc123...
  Subject: Team Meeting - AI
  From: anna@example.com
✓ Event created: Team Meeting - AI
  Link: https://calendar.google.com/calendar/event?eid=...
✓ Marked email as read: abc123

--- Scan complete: 1/1 emails processed ---
```

### Example 2: Continuous Monitoring

```env
RUN_MODE=continuous
SCAN_INTERVAL=30
SEARCH_MODE=config
SEARCH_QUERY=is:unread subject:(meeting OR appointment OR schedule)
```

Every 30 seconds, scans for unread emails about meetings/appointments/schedules.

### Example 3: AI-Powered Search with Smart Event Extraction

**Why use LLM mode?**
- Understands natural language queries
- Extracts specific date, time, and location from email content
- More flexible than rigid search syntax
- Better for complex scheduling emails

**Email example:**
```
To: your.calendar.email@gmail.com
Subject: Project Review Meeting
Body:
Hi Anna,

Let's schedule a meeting to discuss the Gmail Calendar automation project.

Date: Thursday, January 30th, 2025
Time: 2:00 PM - 3:30 PM
Location: Conference Room B (or Zoom if you prefer)

Agenda:
- Review current progress
- Discuss LLM integration benefits
- Plan next development phase

Looking forward to our discussion!
Best regards
```

**Configuration (.env):**
```env
RUN_MODE=once
SEARCH_MODE=llm
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
LLM_SEARCH_PROMPT=Find emails from my manager about next week's meetings
```

**What LLM does:**
1. Converts your natural language prompt to Gmail search query
2. Finds matching emails
3. **Extracts event details from email body:**
   - Title: "Project Review Meeting"
   - Date: January 30, 2025
   - Time: 2:00 PM - 3:30 PM (exact times!)
   - Location: Conference Room B
   - Description: Includes meeting agenda

**Result:**
Calendar event created with **accurate date/time/location** instead of default values!

**Console output:**
```
Using LLM to generate query from: 'Find emails from my manager...'
LLM generated query: is:unread from:manager@company.com subject:(meeting OR appointment) newer_than:7d

--- Starting email scan ---
Found 1 email(s)

Processing email: xyz789...
  Subject: Project Review Meeting
  From: manager@company.com
  Extracting event details with LLM...
✓ Event created: Project Review Meeting
  Link: https://calendar.google.com/calendar/event?eid=...
  Time: 2025-01-30T14:00:00 (extracted from email!)
  Location: Conference Room B (extracted from email!)
✓ Marked email as read

--- Scan complete: 1/1 emails processed ---
```

**LLM Mode Benefits:**
- ✅ Extracts actual meeting times (not default 10 AM)
- ✅ Finds location information
- ✅ Understands context and intent
- ✅ Works with natural language prompts
- ✅ Better for scheduling emails with details

**Cost consideration:** ~$0.03-0.06 per email processed with GPT-4

## Quick Test - Try It Yourself!

Want to see it in action? Follow these steps:

### Step 1: Send yourself a test email

**From:** Your personal email  
**To:** The Gmail account you configured  
**Subject:** `Team Meeting - Test Project`  
**Body:**
```
Hi,

Quick sync about the test project.

See you soon!
```

### Step 2: Configure and run

Make sure your `.env` has:
```env
RUN_MODE=once
SEARCH_MODE=config
SEARCH_QUERY=is:unread subject:meeting
```

### Step 3: Execute

```bash
python main.py
```

### Step 4: Check results

1. **Console** - Should show "Event created" ✓
2. **Gmail** - Email should be marked as read
3. **Google Calendar** - New event should appear!

### To test again:

1. Mark the email as unread in Gmail
2. Run `python main.py` again
3. Event will be created again

---

## Troubleshooting

### Authentication Issues

**Problem:** "Missing credentials.json"
- Download from Google Cloud Console → APIs & Services → Credentials

**Problem:** "Access denied" or "Invalid scope"
- Re-authenticate by deleting `token.pickle` and running again

### Search Returns No Results

**Config Mode:**
- Test query in Gmail web interface first
- Check if emails match ALL criteria (is:unread AND subject:keyword)

**LLM Mode:**
- Verify OPENAI_API_KEY is set
- Check API usage limits
- Review generated query in console output

### Events Not Created

- Check calendar ID (default: 'primary')
- Verify Calendar API is enabled in Google Cloud
- Check calendar permissions

### Continuous Mode Not Stopping

- Press `Ctrl+C` to stop gracefully
- Force quit if needed: `Ctrl+Z` or close terminal

## Security Notes

- **Never commit** `credentials.json` or `token.pickle` to version control
- **Never share** your `OPENAI_API_KEY`
- Keep `.env` file private
- Review OAuth scopes before granting access

## API Costs

### Google APIs
- **Gmail API**: Free (within generous quota limits)
- **Calendar API**: Free (within generous quota limits)
- **This project**: Completely FREE when using Config mode

### OpenAI API (LLM Mode Only)
**When to use LLM mode:**
- Emails with specific dates/times that you want extracted
- Complex scheduling emails
- Natural language search needs

**Costs:**
- GPT-4: ~$0.03-0.06 per email processed
- 100 emails = $3-6
- Only charged when using `SEARCH_MODE=llm`

**How to minimize costs:**
1. Use **Config mode** for simple searches (FREE)
2. Use **LLM mode** only for emails with detailed scheduling info
3. Test with few emails first
4. Consider GPT-3.5-turbo for lower costs (change in `llm_helper.py`)

**Example cost scenarios:**
- Monitoring 10 meeting invites/day with Config mode: **$0/month**
- Processing 5 detailed scheduling emails/day with LLM: **~$5-10/month**
- Processing 100 emails once with LLM: **~$3-6 one-time**

## Support

For issues with:
- **Google APIs**: Check [Google Cloud Console](https://console.cloud.google.com/)
- **OpenAI**: Check [OpenAI Platform](https://platform.openai.com/)
- **Code bugs**: Review error messages and check configuration

## License

MIT License - Free for educational and commercial use

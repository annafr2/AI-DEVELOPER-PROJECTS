# Product Requirements Document (PRD)
# MEM - Mail Excel Manager

**Version:** 1.0
**Last Updated:** October 25, 2025
**Product Owner:** Development Team
**Status:** MVP Complete

---

## 1. Executive Summary

MEM (Mail Excel Manager) is a Python-based automation tool that enables users to fetch, filter, and export Gmail emails to Excel format. The system integrates with Claude AI through the Model Context Protocol (MCP), allowing natural language email management and data extraction.

**Key Value Propositions:**
- Quick email data extraction without manual copying
- Natural language interface via Claude AI
- Structured Excel exports for analysis and reporting
- Secure OAuth2 authentication
- Batch processing of multiple emails

---

## 2. Problem Statement

### Current Challenges

**Problem 1: Manual Email Data Extraction**
- Users spend significant time manually copying email data to spreadsheets
- Copy-paste errors introduce data inconsistencies
- No efficient way to extract data from multiple emails

**Problem 2: Email Organization and Analysis**
- Gmail search is powerful but results aren't easily exportable
- No native way to create structured reports from email data
- Difficult to share email information without forwarding entire threads

**Problem 3: Integration Gaps**
- Gmail doesn't integrate directly with Excel
- Third-party tools are expensive or lack customization
- No AI-assisted email management solutions

### Impact

Without MEM, users face:
- 2-3 hours/week spent on manual email data entry
- Increased error rates in data transcription
- Delayed reporting and analysis
- Inefficient email-based workflows

---

## 3. Goals and Objectives

### Primary Goals

1. **Automate Email Export**
   - Enable one-click email-to-Excel conversion
   - Support Gmail's full search query syntax
   - Handle 100+ emails per batch

2. **Enable AI-Powered Interaction**
   - Integrate with Claude via MCP
   - Support natural language queries
   - Provide intelligent email filtering

3. **Ensure Data Security**
   - Use OAuth2 for secure authentication
   - No email data storage on external servers
   - Local-only processing and export

### Success Metrics

- **Adoption:** 100+ successful email exports in first month
- **Efficiency:** 80% reduction in manual email data entry time
- **Reliability:** 99% successful authentication rate
- **User Satisfaction:** 4.5+ star rating from users

---

## 4. User Personas

### Persona 1: Business Analyst (Emma)

**Demographics:**
- Age: 32
- Role: Business Analyst at tech company
- Tech Savvy: High

**Needs:**
- Extract invoice emails for monthly reports
- Export customer feedback emails for analysis
- Create structured datasets from email communications

**Pain Points:**
- Manually copying data from 50+ invoice emails monthly
- Inconsistent data formats in exports
- Time-consuming email filtering

**Usage Pattern:**
- Daily email exports for specific date ranges
- Weekly invoice compilations
- Monthly comprehensive reports

### Persona 2: Executive Assistant (David)

**Demographics:**
- Age: 28
- Role: Executive Assistant
- Tech Savvy: Medium

**Needs:**
- Organize executive's important emails
- Create email summaries for meetings
- Archive specific email categories

**Pain Points:**
- Difficulty filtering relevant emails
- Manual email organization
- Creating readable email summaries

**Usage Pattern:**
- Daily email organization
- Pre-meeting email summaries
- Weekly archives

### Persona 3: Researcher (Dr. Sarah)

**Demographics:**
- Age: 45
- Role: Academic Researcher
- Tech Savvy: High

**Needs:**
- Extract study participant correspondence
- Organize grant-related emails
- Create audit trails of communications

**Pain Points:**
- Need for structured email records
- Compliance requirements for data retention
- Multiple email accounts to manage

**Usage Pattern:**
- Project-based email exports
- Quarterly compliance reports
- Subject-specific email collections

---

## 5. Features and Requirements

### 5.1 Core Features (MVP)

#### Feature 1: Gmail Authentication
**Description:** Secure OAuth2 authentication with Gmail API

**Requirements:**
- FR-1.1: Support Google OAuth2 authentication flow
- FR-1.2: Store and refresh authentication tokens securely
- FR-1.3: Handle authentication errors gracefully
- FR-1.4: Support token revocation
- FR-1.5: Display authentication status

**Priority:** P0 (Must Have)
**Status:** ✅ Complete

#### Feature 2: Email Fetching
**Description:** Search and retrieve emails based on Gmail query syntax

**Requirements:**
- FR-2.1: Support full Gmail search query syntax
- FR-2.2: Fetch up to 500 emails per query
- FR-2.3: Extract email metadata (sender, subject, date, labels)
- FR-2.4: Parse email body (plain text and HTML)
- FR-2.5: Handle pagination for large result sets
- FR-2.6: Respect Gmail API rate limits
- FR-2.7: Display fetch progress

**Priority:** P0 (Must Have)
**Status:** ✅ Complete

#### Feature 3: Excel Export
**Description:** Export fetched emails to structured Excel files

**Requirements:**
- FR-3.1: Create Excel files with proper formatting
- FR-3.2: Include columns: Date, From, To, Subject, Body Preview, Labels
- FR-3.3: Support custom filename specification
- FR-3.4: Auto-generate timestamp-based filenames
- FR-3.5: Handle special characters in email content
- FR-3.6: Support output directory specification
- FR-3.7: Truncate long email bodies with option for full export

**Priority:** P0 (Must Have)
**Status:** ✅ Complete

#### Feature 4: Command Line Interface
**Description:** CLI for standalone usage without Claude

**Requirements:**
- FR-4.1: `--auth` flag for authentication
- FR-4.2: `--query` parameter for email search
- FR-4.3: `--max` parameter for result limit
- FR-4.4: `--output` parameter for filename
- FR-4.5: `--output-dir` parameter for directory
- FR-4.6: `--profile` flag to show account info
- FR-4.7: `--revoke` flag to revoke authentication
- FR-4.8: `--help` for command documentation
- FR-4.9: `--full-body` flag for complete email bodies

**Priority:** P0 (Must Have)
**Status:** ✅ Complete

#### Feature 5: MCP Server Integration
**Description:** Expose functionality via Model Context Protocol for Claude

**Requirements:**
- FR-5.1: Implement MCP server using official SDK
- FR-5.2: Expose `fetch_gmail_emails` tool
- FR-5.3: Expose `export_emails_to_excel` tool
- FR-5.4: Expose `get_email_details` tool
- FR-5.5: Handle tool parameters and validation
- FR-5.6: Return structured responses
- FR-5.7: Provide error messages in user-friendly format

**Priority:** P0 (Must Have)
**Status:** ✅ Complete

### 5.2 Future Features (Post-MVP)

#### Feature 6: Attachment Handling
**Description:** Download and organize email attachments

**Requirements:**
- FR-6.1: Download attachments to specified directory
- FR-6.2: Organize by sender/date/subject
- FR-6.3: Filter by attachment type
- FR-6.4: Include attachment metadata in Excel
- FR-6.5: Handle large attachment sizes

**Priority:** P1 (Should Have)
**Status:** 📋 Planned

#### Feature 7: Multi-Account Support
**Description:** Manage multiple Gmail accounts

**Requirements:**
- FR-7.1: Switch between multiple authenticated accounts
- FR-7.2: Named account profiles
- FR-7.3: Account-specific configurations
- FR-7.4: Concurrent access to multiple accounts

**Priority:** P2 (Nice to Have)
**Status:** 📋 Planned

#### Feature 8: Advanced Filtering
**Description:** Post-fetch filtering and processing

**Requirements:**
- FR-8.1: Regular expression filtering
- FR-8.2: Custom field extraction
- FR-8.3: Email deduplication
- FR-8.4: Content-based categorization
- FR-8.5: Sentiment analysis integration

**Priority:** P2 (Nice to Have)
**Status:** 📋 Planned

#### Feature 9: Scheduled Exports
**Description:** Automated periodic email exports

**Requirements:**
- FR-9.1: Configure scheduled export tasks
- FR-9.2: Cron job integration
- FR-9.3: Email notifications on completion
- FR-9.4: Incremental exports (only new emails)
- FR-9.5: Export history tracking

**Priority:** P2 (Nice to Have)
**Status:** 📋 Planned

#### Feature 10: Database Integration
**Description:** Store email metadata in local database

**Requirements:**
- FR-10.1: SQLite database for email metadata
- FR-10.2: Full-text search across stored emails
- FR-10.3: Historical analysis and trends
- FR-10.4: Duplicate detection
- FR-10.5: Export from database to Excel

**Priority:** P3 (Won't Have for Now)
**Status:** 📋 Future

---

## 6. User Stories

### Authentication Stories

**US-1:** As a user, I want to authenticate with my Gmail account using OAuth2, so that MEM can access my emails securely.
- **Acceptance Criteria:**
  - ✅ Browser opens for Google authentication
  - ✅ Successful authentication stores token
  - ✅ Token persists between sessions
  - ✅ Error messages show if authentication fails

**US-2:** As a user, I want to revoke MEM's access to my Gmail, so that I can control my data security.
- **Acceptance Criteria:**
  - ✅ `--revoke` command removes stored tokens
  - ✅ Confirmation message displayed
  - ✅ Requires re-authentication for next use

### Email Fetching Stories

**US-3:** As a business analyst, I want to fetch all invoice emails from last month, so that I can create a monthly financial report.
- **Acceptance Criteria:**
  - ✅ Support date-based queries (after:/before:)
  - ✅ Support subject-based filtering
  - ✅ Return emails sorted by date
  - ✅ Display count of fetched emails

**US-4:** As an executive assistant, I want to fetch unread emails from my boss, so that I can prioritize responses.
- **Acceptance Criteria:**
  - ✅ Support `is:unread` filter
  - ✅ Support `from:` filter
  - ✅ Combine multiple query parameters
  - ✅ Show email preview in results

**US-5:** As a researcher, I want to limit results to 100 emails, so that I don't exceed API quotas.
- **Acceptance Criteria:**
  - ✅ `--max` parameter limits results
  - ✅ Default limit is 100
  - ✅ Warning if more emails available
  - ✅ Pagination support for large sets

### Export Stories

**US-6:** As a user, I want to export emails to Excel with all metadata, so that I can analyze them in spreadsheet software.
- **Acceptance Criteria:**
  - ✅ Excel file contains: Date, From, To, Subject, Body, Labels
  - ✅ Proper column headers
  - ✅ Readable formatting
  - ✅ Special characters handled correctly

**US-7:** As a user, I want to specify a custom filename, so that I can organize my exports.
- **Acceptance Criteria:**
  - ✅ `--output` parameter accepts custom filename
  - ✅ Auto-append .xlsx if not provided
  - ✅ Validate filename characters
  - ✅ Handle filename conflicts

**US-8:** As a user, I want auto-generated filenames with timestamps, so that exports don't overwrite each other.
- **Acceptance Criteria:**
  - ✅ Default format: `emails_YYYYMMDD_HHMMSS.xlsx`
  - ✅ Timestamp in local timezone
  - ✅ Unique filenames guaranteed

### Claude Integration Stories

**US-9:** As a Claude user, I want to ask "fetch my invoice emails" in natural language, so that I don't need to learn command syntax.
- **Acceptance Criteria:**
  - ✅ MCP server translates natural language to queries
  - ✅ Claude can call fetch_gmail_emails tool
  - ✅ Results returned to Claude
  - ✅ Error messages in plain English

**US-10:** As a Claude user, I want to say "export those to Excel", so that I can save results without typing commands.
- **Acceptance Criteria:**
  - ✅ Claude can call export_emails_to_excel tool
  - ✅ Context maintained between tool calls
  - ✅ Confirmation message with file path
  - ✅ Handle export errors gracefully

---

## 7. Technical Requirements

### 7.1 System Requirements

**Hardware:**
- Minimum: 2 GB RAM, 100 MB disk space
- Recommended: 4 GB RAM, 500 MB disk space

**Software:**
- Python 3.8 or higher
- Internet connection for Gmail API
- Modern web browser for OAuth authentication

**Operating Systems:**
- ✅ Linux
- ✅ macOS
- ✅ Windows (via WSL recommended)

### 7.2 Dependencies

**Core Dependencies:**
```
google-api-python-client==2.108.0  # Gmail API
google-auth-httplib2==0.2.0         # OAuth HTTP
google-auth-oauthlib==1.2.0         # OAuth flow
openpyxl==3.1.2                      # Excel generation
mcp>=1.0.0                           # MCP protocol
python-dotenv==1.0.0                 # Configuration
```

### 7.3 API Requirements

**Gmail API:**
- API enabled in Google Cloud Console
- OAuth2 credentials (client ID and secret)
- Scopes: `https://www.googleapis.com/auth/gmail.readonly`
- Quotas: 1 billion quota units/day (default)

**Gmail API Usage:**
- List messages: ~5 quota units per call
- Get message: ~5 quota units per call
- Typical query (100 emails): ~505 quota units

### 7.4 Security Requirements

**NFR-1: Authentication**
- Use OAuth2 for all Gmail access
- No password storage
- Token encryption at rest
- Automatic token refresh

**NFR-2: Data Privacy**
- No email data sent to external servers
- Local-only processing
- No analytics or tracking
- User-controlled data deletion

**NFR-3: Credentials Management**
- credentials.json excluded from version control
- token.json protected with file permissions (600)
- Environment variables for sensitive config
- Clear instructions for credential setup

### 7.5 Performance Requirements

**NFR-4: Speed**
- Authentication flow: < 5 seconds
- Fetch 100 emails: < 10 seconds
- Export to Excel: < 5 seconds
- MCP tool response: < 15 seconds total

**NFR-5: Scalability**
- Handle up to 500 emails per query
- Excel files up to 10 MB
- Support concurrent MCP requests
- Graceful degradation under API limits

### 7.6 Reliability Requirements

**NFR-6: Error Handling**
- Graceful handling of network failures
- Clear error messages for users
- Automatic retry on transient failures
- Logging of all errors

**NFR-7: Data Integrity**
- No email data loss during export
- Correct character encoding (UTF-8)
- Preserve email metadata accuracy
- Validate Excel file creation

---

## 8. Success Metrics

### Usage Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Daily Active Users | 10+ | User count running exports |
| Emails Exported per Week | 1,000+ | Total email count |
| Average Emails per Export | 50-100 | Mean per session |
| CLI vs MCP Usage | 50/50 | Usage split |

### Performance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Authentication Success Rate | 99%+ | Successful/total attempts |
| Email Fetch Success Rate | 98%+ | Successful/total queries |
| Export Success Rate | 99%+ | Successful/total exports |
| Average Response Time | < 15s | End-to-end per query |

### Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Data Accuracy | 99.9%+ | Correct data in exports |
| Error Rate | < 1% | Failed operations/total |
| User Satisfaction | 4.5/5 | Survey ratings |
| Bug Reports | < 5/month | Reported issues |

### Adoption Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| First Week Users | 20+ | New authentications |
| Retention (30 days) | 60%+ | Active after 30 days |
| Feature Usage | All features used | CLI + MCP both active |
| Repeat Usage | 3+/week | Sessions per user |

---

## 9. User Experience

### 9.1 CLI Experience

**Ease of Use:**
- Self-documenting help text
- Sensible defaults for all parameters
- Clear progress indicators
- Informative success/error messages

**Example User Flow:**
```bash
# First time - authenticate
./venv/bin/python main.py --auth
# ✅ Browser opens, user authorizes, success message

# Fetch emails
./venv/bin/python main.py --query "is:unread" --max 20
# ✅ Progress shown, export created, file path displayed

# View profile
./venv/bin/python main.py --profile
# ✅ Shows email address and account info
```

### 9.2 Claude Experience

**Natural Language Interaction:**
- No command syntax required
- Context-aware responses
- Intelligent query translation
- Conversational error handling

**Example User Flow:**
```
User: "Claude, get my emails from GitHub in the last week"
Claude: [Calls fetch_gmail_emails]
       "I found 23 emails from GitHub in the last week.
        Would you like me to export them to Excel?"

User: "Yes, name it github_notifications.xlsx"
Claude: [Calls export_emails_to_excel]
       "Done! Exported 23 emails to github_notifications.xlsx"
```

---

## 10. Timeline and Milestones

### Phase 1: MVP (Complete)
**Duration:** Completed
**Status:** ✅ Done

- ✅ Gmail OAuth authentication
- ✅ Email fetching with query support
- ✅ Excel export functionality
- ✅ CLI interface
- ✅ MCP server integration
- ✅ Documentation (README, PLANNING, TASKS, TEST, CLAUDE)

### Phase 2: Enhancement (Planned)
**Duration:** 4-6 weeks
**Status:** 📋 Planned

- 📋 Attachment download support
- 📋 Advanced filtering options
- 📋 Multi-account support
- 📋 Improved error handling
- 📋 Performance optimizations
- 📋 Extended test coverage

### Phase 3: Advanced Features (Future)
**Duration:** 8-12 weeks
**Status:** 📋 Future

- 📋 Scheduled exports
- 📋 Database integration
- 📋 Email content analysis
- 📋 Custom export formats (CSV, JSON)
- 📋 Web interface
- 📋 Team collaboration features

---

## 11. Risks and Mitigation

### Technical Risks

**Risk 1: Gmail API Rate Limits**
- **Probability:** Medium
- **Impact:** High
- **Mitigation:**
  - Implement exponential backoff
  - Cache responses where possible
  - Warn users of quota consumption
  - Implement batch processing

**Risk 2: OAuth Token Expiration**
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:**
  - Automatic token refresh
  - Clear re-authentication flow
  - Token expiry warnings
  - Graceful fallback to re-auth

**Risk 3: Excel File Size Limits**
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:**
  - Limit max emails per export
  - Truncate email bodies by default
  - Split large exports into multiple files
  - Warn about size limits

### Security Risks

**Risk 4: Credential Theft**
- **Probability:** Low
- **Impact:** High
- **Mitigation:**
  - File permission enforcement (600)
  - No credential logging
  - gitignore for sensitive files
  - User education on security

**Risk 5: Email Data Exposure**
- **Probability:** Low
- **Impact:** High
- **Mitigation:**
  - Local-only processing
  - No cloud storage of emails
  - Encrypted token storage
  - Clear data handling policies

### Operational Risks

**Risk 6: User Authentication Confusion**
- **Probability:** Medium
- **Impact:** Low
- **Mitigation:**
  - Clear documentation
  - Step-by-step auth guide
  - Helpful error messages
  - Video tutorials

**Risk 7: Dependency Updates Breaking Changes**
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:**
  - Pin dependency versions
  - Regular testing of updates
  - Changelog monitoring
  - Backward compatibility testing

---

## 12. Compliance and Legal

### Data Privacy

- **GDPR Compliance:** No user data stored; user-controlled exports
- **Data Minimization:** Only fetch requested emails
- **Right to Deletion:** User can revoke access anytime
- **Data Portability:** Excel exports enable easy data transfer

### Google Compliance

- **OAuth2 Requirements:** Fully compliant with Google OAuth2
- **API Terms of Service:** Adheres to Gmail API ToS
- **Branding Guidelines:** Proper Google branding in auth flow
- **Security Assessment:** May require verification for public release

---

## 13. Support and Maintenance

### Documentation

- ✅ README.md - Quick start guide
- ✅ PLANNING.md - Architecture details
- ✅ CLAUDE.md - MCP integration guide
- ✅ TASKS.md - Implementation roadmap
- ✅ TEST.md - Testing strategy
- ✅ PRD.md - This document

### User Support Channels

- GitHub Issues - Bug reports and feature requests
- Documentation - Self-service help
- Email Support - Direct assistance
- Community Forum - User discussions (future)

### Maintenance Plan

- **Weekly:** Monitor error logs
- **Monthly:** Dependency updates
- **Quarterly:** Feature releases
- **As-needed:** Security patches

---

## 14. Future Roadmap

### Short Term (3-6 months)

1. **Attachment Support**
   - Download and organize attachments
   - Include in Excel exports
   - Filter by file type

2. **Enhanced Filtering**
   - Regular expressions
   - Custom field extraction
   - Content-based sorting

3. **Performance Improvements**
   - Caching layer
   - Parallel processing
   - Optimized queries

### Medium Term (6-12 months)

1. **Multi-Account Support**
   - Switch between accounts
   - Unified search across accounts
   - Per-account configurations

2. **Scheduled Exports**
   - Cron job integration
   - Automated reports
   - Email notifications

3. **Database Integration**
   - Local SQLite storage
   - Historical analysis
   - Advanced querying

### Long Term (12+ months)

1. **Web Interface**
   - Browser-based UI
   - Visual query builder
   - Real-time previews

2. **Team Features**
   - Shared configurations
   - Collaborative filtering
   - Access controls

3. **Analytics Dashboard**
   - Email statistics
   - Trend analysis
   - Visualization tools

---

## 15. Appendix

### A. Gmail Query Syntax Reference

| Syntax | Description | Example |
|--------|-------------|---------|
| `from:` | From specific sender | `from:example@gmail.com` |
| `to:` | To specific recipient | `to:user@company.com` |
| `subject:` | Subject contains keyword | `subject:invoice` |
| `after:` | After date | `after:2024/01/01` |
| `before:` | Before date | `before:2024/12/31` |
| `is:unread` | Unread emails | `is:unread` |
| `is:starred` | Starred emails | `is:starred` |
| `has:attachment` | Has attachments | `has:attachment` |
| `label:` | Specific label | `label:work` |
| `newer_than:` | Relative date | `newer_than:7d` |
| `older_than:` | Relative date | `older_than:1m` |
| `OR` | Logical OR | `from:a OR from:b` |
| Space | Logical AND | `from:a subject:b` |

### B. Excel Export Format

**Columns:**
1. **Date** - Email sent/received date (YYYY-MM-DD HH:MM:SS)
2. **From** - Sender email address
3. **To** - Recipient email addresses (comma-separated)
4. **Subject** - Email subject line
5. **Body** - Email body (truncated or full based on flag)
6. **Labels** - Gmail labels (comma-separated)

**Formatting:**
- Header row with bold text
- Auto-sized columns
- Date formatted as timestamp
- UTF-8 encoding for special characters

### C. Error Codes

| Code | Message | Resolution |
|------|---------|------------|
| AUTH_001 | Credentials file not found | Download credentials.json |
| AUTH_002 | Authentication failed | Re-run --auth command |
| AUTH_003 | Token expired | Automatic refresh or re-auth |
| FETCH_001 | Invalid query syntax | Check query format |
| FETCH_002 | API rate limit exceeded | Wait and retry |
| FETCH_003 | No emails found | Verify query matches emails |
| EXPORT_001 | Failed to create file | Check write permissions |
| EXPORT_002 | Invalid filename | Use valid characters |
| MCP_001 | Server connection failed | Check MCP configuration |
| MCP_002 | Tool execution error | Check tool parameters |

### D. API Quota Details

**Gmail API Quotas (Default):**
- **Per-user rate limit:** 250 quota units/user/second
- **Daily quota:** 1 billion quota units/day
- **Queries per day:** ~2 million (assuming 500 units per query)

**Quota Units per Operation:**
- `users.messages.list`: 5 units
- `users.messages.get`: 5 units
- `users.getProfile`: 1 unit

**Example Calculation:**
- Fetch 100 emails: 5 (list) + (100 × 5 (get)) = 505 units
- Daily quota allows: ~2 million email fetches

### E. Development Environment Setup

**Quick Start:**
```bash
# Clone repository
git clone [repository-url]
cd MEM

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup credentials
# Place credentials.json in project root

# Authenticate
python main.py --auth

# Test
python main.py --query "is:inbox" --max 5
```

### F. MCP Configuration Example

```json
{
  "mcpServers": {
    "mem-gmail": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_server.py"],
      "env": {
        "GMAIL_CREDENTIALS_PATH": "/path/to/credentials.json",
        "MEM_DEBUG": "0"
      }
    }
  }
}
```

---

## Document Control

**Version History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-25 | Development Team | Initial PRD - MVP Complete |

**Approvals:**

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product Owner | TBD | - | - |
| Technical Lead | TBD | - | - |
| Stakeholder | TBD | - | - |

**Distribution:**
- Development Team
- Product Stakeholders
- Documentation Repository

---

**End of Document**

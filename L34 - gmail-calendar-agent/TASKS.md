# Development Tasks

## Project: Gmail to Calendar Automation

---

## Phase 1: Setup and Configuration

### Task 1.1: Google Cloud Project Setup
- [ ] Create new Google Cloud project
- [ ] Enable Gmail API
- [ ] Enable Google Calendar API
- [ ] Configure OAuth consent screen
- [ ] Create OAuth 2.0 credentials
- [ ] Download credentials.json
- [ ] Place credentials.json in project root

**Estimated Time:** 20 minutes  
**Priority:** HIGH  
**Dependencies:** None

### Task 1.2: Project Environment Setup
- [ ] Create project directory
- [ ] Install Python 3.8+ (if needed)
- [ ] Create virtual environment
- [ ] Install dependencies from requirements.txt
- [ ] Copy .env.example to .env
- [ ] Configure basic settings in .env

**Estimated Time:** 15 minutes  
**Priority:** HIGH  
**Dependencies:** Task 1.1

---

## Phase 2: Core Development

### Task 2.1: Configuration Module (config.py)
- [ ] Create Config class
- [ ] Load environment variables
- [ ] Define API scopes
- [ ] Add configuration validation
- [ ] Add display method for debugging
- [ ] Test with different configurations

**Estimated Time:** 30 minutes  
**Priority:** HIGH  
**Dependencies:** Task 1.2

### Task 2.2: Authentication Module (auth.py)
- [ ] Implement OAuth 2.0 flow
- [ ] Add token caching (pickle)
- [ ] Add token refresh logic
- [ ] Create service builder functions
- [ ] Add connection test function
- [ ] Test authentication flow

**Estimated Time:** 45 minutes  
**Priority:** HIGH  
**Dependencies:** Task 2.1

### Task 2.3: Gmail Scanner Module (gmail_scanner.py)
- [ ] Implement search_emails function
- [ ] Implement get_email_content function
- [ ] Implement mark_as_read function
- [ ] Add error handling for API calls
- [ ] Test with various search queries
- [ ] Handle edge cases (empty results, invalid IDs)

**Estimated Time:** 60 minutes  
**Priority:** HIGH  
**Dependencies:** Task 2.2

### Task 2.4: Calendar Manager Module (calendar_manager.py)
- [ ] Implement create_event_from_email function
- [ ] Implement build_event_from_email function
- [ ] Implement build_event_from_details function
- [ ] Add list_upcoming_events for testing
- [ ] Handle timezone conversion
- [ ] Test event creation

**Estimated Time:** 60 minutes  
**Priority:** HIGH  
**Dependencies:** Task 2.2

### Task 2.5: LLM Helper Module (llm_helper.py)
- [ ] Implement generate_gmail_query function
- [ ] Implement extract_event_details function
- [ ] Add error handling for OpenAI API
- [ ] Add fallback for missing API key
- [ ] Test with various prompts
- [ ] Optimize token usage

**Estimated Time:** 45 minutes  
**Priority:** MEDIUM  
**Dependencies:** Task 2.1

### Task 2.6: Main Application (main.py)
- [ ] Implement main function
- [ ] Implement run_once mode
- [ ] Implement run_continuous mode
- [ ] Implement process_emails workflow
- [ ] Add graceful shutdown handling
- [ ] Add progress logging

**Estimated Time:** 45 minutes  
**Priority:** HIGH  
**Dependencies:** Tasks 2.3, 2.4, 2.5

---

## Phase 3: Testing

### Task 3.1: Unit Testing
- [ ] Test configuration validation
- [ ] Test authentication flow
- [ ] Test Gmail search functions
- [ ] Test calendar event creation
- [ ] Test LLM query generation
- [ ] Fix bugs found during testing

**Estimated Time:** 90 minutes  
**Priority:** HIGH  
**Dependencies:** All Phase 2 tasks

### Task 3.2: Integration Testing
- [ ] Test config mode end-to-end
- [ ] Test LLM mode end-to-end
- [ ] Test single-run mode
- [ ] Test continuous mode
- [ ] Test error scenarios
- [ ] Test with real emails

**Estimated Time:** 60 minutes  
**Priority:** HIGH  
**Dependencies:** Task 3.1

### Task 3.3: Edge Case Testing
- [ ] Empty inbox (no matching emails)
- [ ] Invalid search query
- [ ] Emails without body content
- [ ] Very long emails
- [ ] Special characters in subject
- [ ] Network interruptions

**Estimated Time:** 45 minutes  
**Priority:** MEDIUM  
**Dependencies:** Task 3.2

---

## Phase 4: Documentation

### Task 4.1: README.md
- [ ] Write installation instructions
- [ ] Document configuration options
- [ ] Add usage examples
- [ ] Create troubleshooting section
- [ ] Add security notes
- [ ] Review and polish

**Estimated Time:** 60 minutes  
**Priority:** HIGH  
**Dependencies:** Task 3.2

### Task 4.2: PRD.md
- [ ] Define product goals
- [ ] List functional requirements
- [ ] List non-functional requirements
- [ ] Document system architecture
- [ ] Define success criteria
- [ ] Review completeness

**Estimated Time:** 45 minutes  
**Priority:** MEDIUM  
**Dependencies:** All Phase 2 tasks

### Task 4.3: Code Documentation
- [ ] Add docstrings to all functions
- [ ] Add inline comments for complex logic
- [ ] Document configuration options
- [ ] Add usage examples in comments
- [ ] Review code readability

**Estimated Time:** 30 minutes  
**Priority:** MEDIUM  
**Dependencies:** All Phase 2 tasks

---

## Phase 5: Polish and Optimization

### Task 5.1: Error Message Improvement
- [ ] Make error messages user-friendly
- [ ] Add suggestions for common errors
- [ ] Improve logging format
- [ ] Add debug mode option
- [ ] Test error messages with users

**Estimated Time:** 30 minutes  
**Priority:** LOW  
**Dependencies:** Task 3.2

### Task 5.2: Performance Optimization
- [ ] Reduce API calls where possible
- [ ] Optimize token usage for LLM
- [ ] Add caching where appropriate
- [ ] Profile memory usage
- [ ] Optimize continuous mode performance

**Estimated Time:** 45 minutes  
**Priority:** LOW  
**Dependencies:** Task 3.2

### Task 5.3: Code Cleanup
- [ ] Remove debug print statements
- [ ] Ensure consistent code style
- [ ] Remove unused imports
- [ ] Organize imports
- [ ] Final code review

**Estimated Time:** 20 minutes  
**Priority:** LOW  
**Dependencies:** All development tasks

---

## Homework Submission Checklist

### Before Submission
- [ ] All code files under 150 lines
- [ ] All modules tested independently
- [ ] End-to-end testing completed
- [ ] README.md is clear and complete
- [ ] PRD.md documents all features
- [ ] .env.example has all options documented
- [ ] No credentials committed to repo
- [ ] Code follows Python style guidelines

### Required Deliverables
- [ ] Source code (all .py files)
- [ ] Configuration files (.env.example)
- [ ] Documentation (README, PRD, TASKS)
- [ ] Requirements.txt
- [ ] .gitignore
- [ ] Demo video or screenshots (optional)

### Demonstration Items
- [ ] Show config mode working
- [ ] Show LLM mode working (if API key available)
- [ ] Show single-run mode
- [ ] Show continuous mode
- [ ] Show email marked as read
- [ ] Show event created in calendar

---

## Timeline Estimate

| Phase | Tasks | Estimated Time | Priority |
|-------|-------|----------------|----------|
| Phase 1 | Setup | 35 min | HIGH |
| Phase 2 | Development | 4h 45min | HIGH |
| Phase 3 | Testing | 3h 15min | HIGH |
| Phase 4 | Documentation | 2h 15min | MEDIUM |
| Phase 5 | Polish | 1h 35min | LOW |
| **Total** | | **~12 hours** | |

**Recommended Schedule:**
- Day 1 (2-3 hours): Phases 1-2 (Setup + Core Development)
- Day 2 (3-4 hours): Phase 3 (Testing) + Phase 2 fixes
- Day 3 (2-3 hours): Phase 4 (Documentation)
- Day 4 (1-2 hours): Phase 5 (Polish) + Final testing

---

## Risk Management

### High Risk Items
1. **Google API Authentication Issues**
   - Mitigation: Follow official Google documentation exactly
   - Backup: Test authentication separately first

2. **OpenAI API Costs**
   - Mitigation: Use GPT-3.5-turbo for development
   - Backup: Test with few emails initially

3. **Gmail Search Query Complexity**
   - Mitigation: Test queries in Gmail web UI first
   - Backup: Start with simple queries, add complexity gradually

### Medium Risk Items
1. **Timezone Handling**
   - Current: Uses UTC only
   - Future: Add timezone configuration

2. **Email Parsing Accuracy**
   - Complex email formats may not parse correctly
   - Test with various email types

3. **Event Duplication**
   - Same email processed multiple times
   - Mark as read immediately after processing

---

## Success Metrics

### Functionality
- ✅ All required features working
- ✅ Both modes (config/llm) functional
- ✅ No critical bugs
- ✅ Error handling works

### Code Quality
- ✅ All files under 150 lines
- ✅ Clear function names
- ✅ Proper error handling
- ✅ Good documentation

### User Experience
- ✅ Easy setup process
- ✅ Clear error messages
- ✅ Helpful README
- ✅ Works as expected

---

## Notes for Development

### Best Practices
- Test each module independently before integration
- Commit code frequently
- Keep functions small and focused
- Use meaningful variable names
- Handle errors gracefully
- Log important events

### Common Pitfalls to Avoid
- Hardcoding credentials
- Ignoring API rate limits
- Not handling network errors
- Forgetting to mark emails as read
- Creating duplicate events
- Poor error messages

### Testing Tips
- Use a test Gmail account
- Start with simple search queries
- Test with few emails first
- Monitor API quota usage
- Test both success and failure cases
- Test edge cases thoroughly

---

## Contact and Support

For help with:
- **Google APIs**: Google Cloud Console documentation
- **OpenAI API**: OpenAI platform documentation
- **Python**: Official Python documentation
- **Code issues**: Review error messages, check logs

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 2026 | Initial task breakdown |


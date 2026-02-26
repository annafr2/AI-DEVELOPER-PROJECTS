"""
Gmail to Calendar Automation - Main Application
Scans Gmail and creates calendar events based on configuration
"""
import time
import sys
from config import Config
from auth import get_google_services
from gmail_scanner import search_emails, get_email_content, mark_as_read
from calendar_manager import create_event_from_email
from llm_helper import extract_event_details

def process_emails(gmail_service, calendar_service):
    """
    Main email processing workflow
    
    Args:
        gmail_service: Authenticated Gmail API service
        calendar_service: Authenticated Calendar API service
    
    Returns:
        int: Number of emails processed
    """
    print("\n--- Starting email scan ---")
    
    # Search for emails
    messages = search_emails(gmail_service)
    
    if not messages:
        return 0
    
    processed_count = 0
    
    for msg in messages:
        message_id = msg['id']
        print(f"\nProcessing email: {message_id}")
        
        # Get email content
        email_data = get_email_content(gmail_service, message_id)
        
        if not email_data:
            print("  ✗ Failed to retrieve email content")
            continue
        
        print(f"  Subject: {email_data['subject']}")
        print(f"  From: {email_data['sender']}")
        
        # Extract event details using LLM if available
        event_details = None
        if Config.OPENAI_API_KEY and Config.SEARCH_MODE == 'llm':
            print("  Extracting event details with LLM...")
            event_details = extract_event_details(email_data['body'])
        
        # Create calendar event
        event = create_event_from_email(calendar_service, email_data, event_details)
        
        if event:
            # Mark email as read
            mark_as_read(gmail_service, message_id)
            processed_count += 1
        else:
            print("  ✗ Failed to create calendar event")
    
    print(f"\n--- Scan complete: {processed_count}/{len(messages)} emails processed ---")
    return processed_count

def run_once(gmail_service, calendar_service):
    """Run single scan"""
    print("\n=== RUNNING IN SINGLE SCAN MODE ===")
    process_emails(gmail_service, calendar_service)
    print("\nSingle scan completed. Exiting.")

def run_continuous(gmail_service, calendar_service):
    """Run continuous scanning"""
    print(f"\n=== RUNNING IN CONTINUOUS MODE ===")
    print(f"Scanning every {Config.SCAN_INTERVAL} seconds")
    print("Press Ctrl+C to stop\n")
    
    try:
        iteration = 1
        while True:
            print(f"\n[Iteration {iteration}]")
            process_emails(gmail_service, calendar_service)
            
            print(f"\nWaiting {Config.SCAN_INTERVAL} seconds until next scan...")
            time.sleep(Config.SCAN_INTERVAL)
            iteration += 1
            
    except KeyboardInterrupt:
        print("\n\nStopping continuous mode...")
        print("Goodbye!")

def main():
    """Main application entry point"""
    print("=" * 50)
    print("Gmail to Calendar Automation")
    print("=" * 50)
    
    # Validate configuration
    errors = Config.validate()
    if errors:
        print("\n❌ Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease fix configuration and try again.")
        sys.exit(1)
    
    # Display configuration
    Config.display()
    
    # Authenticate with Google APIs
    print("Authenticating with Google APIs...")
    try:
        gmail_service, calendar_service = get_google_services()
        print("✓ Authentication successful\n")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        sys.exit(1)
    
    # Run based on mode
    if Config.RUN_MODE == 'once':
        run_once(gmail_service, calendar_service)
    else:
        run_continuous(gmail_service, calendar_service)

if __name__ == "__main__":
    main()

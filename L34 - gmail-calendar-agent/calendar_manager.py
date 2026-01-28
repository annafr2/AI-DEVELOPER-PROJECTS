"""
Calendar Manager Module
Handles Google Calendar API operations: create events
"""
from datetime import datetime, timedelta
from config import Config

def create_event_from_email(calendar_service, email_data, event_details=None):
    """
    Create calendar event from email data
    
    Args:
        calendar_service: Authenticated Calendar API service
        email_data: Email information dict
        event_details: Optional parsed event details from LLM
    
    Returns:
        dict: Created event or None if failed
    """
    try:
        # Use LLM-extracted details if available, otherwise use email data
        if event_details:
            event = build_event_from_details(event_details, email_data)
        else:
            event = build_event_from_email(email_data)
        
        created_event = calendar_service.events().insert(
            calendarId=Config.CALENDAR_ID,
            body=event
        ).execute()
        
        print(f"✓ Event created: {created_event.get('summary')}")
        print(f"  Link: {created_event.get('htmlLink')}")
        
        return created_event
        
    except Exception as e:
        print(f"Error creating calendar event: {e}")
        return None

def build_event_from_details(event_details, email_data):
    """
    Build calendar event from LLM-extracted details
    
    Args:
        event_details: Parsed event information
        email_data: Original email data
    
    Returns:
        dict: Calendar event object
    """
    # Default to tomorrow 10 AM if no time specified
    default_start = datetime.now() + timedelta(days=1)
    default_start = default_start.replace(hour=10, minute=0, second=0, microsecond=0)
    
    event = {
        'summary': event_details.get('title') or email_data['subject'],
        'description': event_details.get('description') or email_data['snippet'],
        'start': {
            'dateTime': event_details.get('start_time') or default_start.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': event_details.get('end_time') or (default_start + timedelta(hours=1)).isoformat(),
            'timeZone': 'UTC',
        },
        'source': {
            'title': f"From: {email_data['sender']}",
            'url': f"https://mail.google.com/mail/#inbox/{email_data['id']}"
        }
    }
    
    if event_details.get('location'):
        event['location'] = event_details['location']
    
    return event

def build_event_from_email(email_data):
    """
    Build basic calendar event from email data
    
    Args:
        email_data: Email information dict
    
    Returns:
        dict: Calendar event object
    """
    # Default: tomorrow at 10 AM for 1 hour
    start_time = datetime.now() + timedelta(days=1)
    start_time = start_time.replace(hour=10, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=1)
    
    event = {
        'summary': email_data['subject'],
        'description': f"Email from: {email_data['sender']}\n\n{email_data['snippet']}",
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'UTC',
        },
        'source': {
            'title': f"From: {email_data['sender']}",
            'url': f"https://mail.google.com/mail/#inbox/{email_data['id']}"
        }
    }
    
    return event

def list_upcoming_events(calendar_service, max_results=10):
    """
    List upcoming calendar events (for testing)
    
    Args:
        calendar_service: Authenticated Calendar API service
        max_results: Maximum number of events to return
    """
    try:
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = calendar_service.events().list(
            calendarId=Config.CALENDAR_ID,
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            print('No upcoming events found.')
            return
        
        print(f"\nUpcoming {len(events)} events:")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"  - {start}: {event['summary']}")
            
    except Exception as e:
        print(f"Error listing events: {e}")

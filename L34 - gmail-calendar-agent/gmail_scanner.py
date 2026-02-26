"""
Gmail Scanner Module
Handles Gmail API operations: search, read, mark as read
"""
import base64
from email.mime.text import MIMEText
from config import Config
from llm_helper import generate_gmail_query

def get_search_query():
    """
    Get Gmail search query based on configuration mode
    
    Returns:
        str: Gmail search query
    """
    if Config.SEARCH_MODE == 'llm':
        print(f"Using LLM to generate query from: '{Config.LLM_SEARCH_PROMPT}'")
        return generate_gmail_query(Config.LLM_SEARCH_PROMPT)
    else:
        print(f"Using config query: '{Config.SEARCH_QUERY}'")
        return Config.SEARCH_QUERY

def search_emails(gmail_service):
    """
    Search Gmail for emails matching query
    
    Args:
        gmail_service: Authenticated Gmail API service
    
    Returns:
        list: List of message IDs
    """
    try:
        query = get_search_query()
        
        results = gmail_service.users().messages().list(
            userId='me',
            q=query,
            maxResults=10
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            print("No emails found matching query")
            return []
        
        print(f"Found {len(messages)} email(s)")
        return messages
        
    except Exception as e:
        print(f"Error searching emails: {e}")
        return []

def get_email_content(gmail_service, message_id):
    """
    Get full email content including subject, sender, body
    
    Args:
        gmail_service: Authenticated Gmail API service
        message_id: Gmail message ID
    
    Returns:
        dict: Email data (subject, sender, body, snippet, id)
    """
    try:
        message = gmail_service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()
        
        headers = message['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown')
        
        # Extract body
        body = ""
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
        elif 'body' in message['payload'] and 'data' in message['payload']['body']:
            body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
        
        return {
            'id': message_id,
            'subject': subject,
            'sender': sender,
            'body': body,
            'snippet': message.get('snippet', '')
        }
        
    except Exception as e:
        print(f"Error getting email content: {e}")
        return None

def mark_as_read(gmail_service, message_id):
    """
    Mark email as read
    
    Args:
        gmail_service: Authenticated Gmail API service
        message_id: Gmail message ID
    """
    try:
        gmail_service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        print(f"✓ Marked email as read: {message_id}")
        
    except Exception as e:
        print(f"Error marking email as read: {e}")

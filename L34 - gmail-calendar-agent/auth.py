"""
Google API Authentication Module
Handles OAuth2 authentication for Gmail and Calendar APIs
"""
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import Config

def get_google_services():
    """
    Authenticate and return Gmail and Calendar service objects
    
    Returns:
        tuple: (gmail_service, calendar_service)
    """
    creds = None
    
    # Load existing token if available
    if os.path.exists(Config.TOKEN_FILE):
        with open(Config.TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing access token...")
            creds.refresh(Request())
        else:
            print("Initiating new authentication flow...")
            print("A browser window will open for authorization")
            flow = InstalledAppFlow.from_client_secrets_file(
                Config.CREDENTIALS_FILE, 
                Config.SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open(Config.TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        print("Authentication successful!")
    
    # Build service objects
    gmail_service = build('gmail', 'v1', credentials=creds)
    calendar_service = build('calendar', 'v3', credentials=creds)
    
    return gmail_service, calendar_service

def test_connection():
    """Test API connection by fetching user profile"""
    try:
        gmail_service, calendar_service = get_google_services()
        
        # Test Gmail
        profile = gmail_service.users().getProfile(userId='me').execute()
        print(f"✓ Gmail connected: {profile['emailAddress']}")
        
        # Test Calendar
        calendar_list = calendar_service.calendarList().list().execute()
        print(f"✓ Calendar connected: {len(calendar_list.get('items', []))} calendars found")
        
        return True
    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        return False

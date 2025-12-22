"""
Gmail OAuth Authentication Handler

This module handles OAuth2 authentication flow for Gmail API access.
It manages token storage, refresh, and provides an authenticated Gmail service.
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Optional

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Token storage file
TOKEN_FILE = 'token.pickle'

# Credentials file (downloaded from Google Cloud Console)
CREDENTIALS_FILE = 'credentials.json'


class GmailAuthenticator:
    """Handles Gmail OAuth2 authentication and service creation."""

    def __init__(self, credentials_path: str = CREDENTIALS_FILE, token_path: str = TOKEN_FILE):
        """
        Initialize the authenticator.

        Args:
            credentials_path: Path to OAuth2 credentials JSON file
            token_path: Path to store/load authentication token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.creds: Optional[Credentials] = None

    def authenticate(self) -> Credentials:
        """
        Authenticate with Gmail API using OAuth2.

        Returns:
            Authenticated credentials object

        Raises:
            FileNotFoundError: If credentials file is not found
            Exception: If authentication fails
        """
        # Check if we have stored credentials
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.creds = pickle.load(token)

        # If credentials don't exist or are invalid, authenticate
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                # Refresh expired token
                print("Refreshing expired token...")
                self.creds.refresh(Request())
            else:
                # Run OAuth flow
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_path}\n"
                        "Please download OAuth2 credentials from Google Cloud Console."
                    )

                print("Starting OAuth2 authentication flow...")
                print("A browser window will open for authorization.")

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            # Save credentials for future use
            with open(self.token_path, 'wb') as token:
                pickle.dump(self.creds, token)

            print("Authentication successful!")

        return self.creds

    def get_gmail_service(self):
        """
        Get authenticated Gmail API service.

        Returns:
            Gmail API service object
        """
        if not self.creds:
            self.authenticate()

        service = build('gmail', 'v1', credentials=self.creds)
        return service

    def revoke_credentials(self) -> bool:
        """
        Revoke stored credentials and delete token file.

        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(self.token_path):
                os.remove(self.token_path)
                print(f"Token file removed: {self.token_path}")
                return True
            else:
                print("No token file found.")
                return False
        except Exception as e:
            print(f"Error revoking credentials: {e}")
            return False


def main():
    """Test authentication flow."""
    print("Gmail OAuth Authenticator Test")
    print("-" * 50)

    authenticator = GmailAuthenticator()

    try:
        creds = authenticator.authenticate()
        print(f"Authentication successful!")
        print(f"Token valid: {creds.valid}")
        print(f"Token expiry: {creds.expiry}")

        # Test service creation
        service = authenticator.get_gmail_service()
        print(f"Gmail service created successfully!")

        # Test API call - get user profile
        profile = service.users().getProfile(userId='me').execute()
        print(f"Email: {profile.get('emailAddress')}")
        print(f"Total messages: {profile.get('messagesTotal')}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Authentication failed: {e}")


if __name__ == "__main__":
    main()

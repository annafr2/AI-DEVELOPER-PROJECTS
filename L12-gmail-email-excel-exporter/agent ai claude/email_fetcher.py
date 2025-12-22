"""
Gmail Email Fetcher

This module fetches emails from Gmail API based on search queries
and parses them into structured data.
"""

import base64
import re
from datetime import datetime
from typing import List, Dict, Optional, Any
from email.utils import parsedate_to_datetime


class EmailFetcher:
    """Handles fetching and parsing emails from Gmail API."""

    def __init__(self, gmail_service):
        """
        Initialize email fetcher.

        Args:
            gmail_service: Authenticated Gmail API service object
        """
        self.service = gmail_service

    def search_emails(
        self,
        query: str,
        max_results: int = 100,
        user_id: str = 'me'
    ) -> List[Dict[str, Any]]:
        """
        Search for emails matching a query.

        Args:
            query: Gmail search query (e.g., "from:example@gmail.com")
            max_results: Maximum number of emails to fetch
            user_id: Gmail user ID (default: 'me')

        Returns:
            List of email dictionaries with parsed data

        Raises:
            Exception: If API call fails
        """
        print(f"Searching emails with query: '{query}'")
        print(f"Max results: {max_results}")

        try:
            emails = []
            page_token = None

            while len(emails) < max_results:
                # Fetch message list
                results = self.service.users().messages().list(
                    userId=user_id,
                    q=query,
                    maxResults=min(max_results - len(emails), 500),
                    pageToken=page_token
                ).execute()

                messages = results.get('messages', [])

                if not messages:
                    break

                print(f"Found {len(messages)} messages in this batch...")

                # Fetch full details for each message
                for msg in messages:
                    email_data = self.get_email_details(msg['id'], user_id)
                    if email_data:
                        emails.append(email_data)

                    if len(emails) >= max_results:
                        break

                # Check for next page
                page_token = results.get('nextPageToken')
                if not page_token:
                    break

            print(f"Total emails fetched: {len(emails)}")
            return emails

        except Exception as e:
            print(f"Error searching emails: {e}")
            raise

    def get_email_details(
        self,
        message_id: str,
        user_id: str = 'me'
    ) -> Optional[Dict[str, Any]]:
        """
        Get full details of a specific email.

        Args:
            message_id: Gmail message ID
            user_id: Gmail user ID (default: 'me')

        Returns:
            Dictionary with email details or None if error

        Raises:
            Exception: If API call fails
        """
        try:
            message = self.service.users().messages().get(
                userId=user_id,
                id=message_id,
                format='full'
            ).execute()

            return self._parse_email(message)

        except Exception as e:
            print(f"Error fetching email {message_id}: {e}")
            return None

    def _parse_email(self, message: Dict) -> Dict[str, Any]:
        """
        Parse Gmail API message into structured format.

        Args:
            message: Gmail API message object

        Returns:
            Dictionary with parsed email data
        """
        headers = message['payload'].get('headers', [])

        # Extract header values
        subject = self._get_header(headers, 'Subject') or '(No Subject)'
        from_addr = self._get_header(headers, 'From') or ''
        to_addr = self._get_header(headers, 'To') or ''
        date_str = self._get_header(headers, 'Date') or ''
        cc_addr = self._get_header(headers, 'Cc') or ''

        # Parse date
        try:
            date_obj = parsedate_to_datetime(date_str) if date_str else None
            date_formatted = date_obj.strftime('%Y-%m-%d %H:%M:%S') if date_obj else ''
        except Exception:
            date_formatted = date_str

        # Extract body
        body = self._get_email_body(message['payload'])

        # Extract labels
        labels = message.get('labelIds', [])

        # Check for attachments
        has_attachment = self._has_attachments(message['payload'])

        # Message metadata
        message_id = message['id']
        thread_id = message['threadId']
        snippet = message.get('snippet', '')

        return {
            'message_id': message_id,
            'thread_id': thread_id,
            'date': date_formatted,
            'from': from_addr,
            'to': to_addr,
            'cc': cc_addr,
            'subject': subject,
            'snippet': snippet,
            'body': body,
            'labels': ', '.join(labels),
            'has_attachment': has_attachment,
        }

    def _get_header(self, headers: List[Dict], name: str) -> Optional[str]:
        """
        Get header value by name.

        Args:
            headers: List of header dictionaries
            name: Header name to find

        Returns:
            Header value or None
        """
        for header in headers:
            if header.get('name', '').lower() == name.lower():
                return header.get('value')
        return None

    def _get_email_body(self, payload: Dict) -> str:
        """
        Extract email body from payload.

        Args:
            payload: Gmail message payload

        Returns:
            Email body text
        """
        body = ''

        # Try to get body from payload data
        if 'body' in payload and 'data' in payload['body']:
            body = self._decode_body(payload['body']['data'])

        # If body is empty, check parts (multipart messages)
        elif 'parts' in payload:
            body = self._get_body_from_parts(payload['parts'])

        return body

    def _get_body_from_parts(self, parts: List[Dict]) -> str:
        """
        Extract body from multipart message.

        Args:
            parts: List of message parts

        Returns:
            Combined body text
        """
        body = ''

        for part in parts:
            mime_type = part.get('mimeType', '')

            # Prefer plain text
            if mime_type == 'text/plain':
                if 'data' in part.get('body', {}):
                    body = self._decode_body(part['body']['data'])
                    break

            # Fallback to HTML
            elif mime_type == 'text/html' and not body:
                if 'data' in part.get('body', {}):
                    html_body = self._decode_body(part['body']['data'])
                    body = self._html_to_text(html_body)

            # Recursively check nested parts
            elif 'parts' in part:
                body = self._get_body_from_parts(part['parts'])
                if body:
                    break

        return body

    def _decode_body(self, data: str) -> str:
        """
        Decode base64url encoded body data.

        Args:
            data: Base64url encoded string

        Returns:
            Decoded text
        """
        try:
            # Gmail uses base64url encoding
            decoded = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            return decoded
        except Exception as e:
            print(f"Error decoding body: {e}")
            return ""

    def _html_to_text(self, html: str) -> str:
        """
        Convert HTML to plain text (simple version).

        Args:
            html: HTML string

        Returns:
            Plain text
        """
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        # Decode HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        return text.strip()

    def _has_attachments(self, payload: Dict) -> bool:
        """
        Check if message has attachments.

        Args:
            payload: Gmail message payload

        Returns:
            True if has attachments, False otherwise
        """
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('filename'):
                    return True
                # Check nested parts
                if 'parts' in part:
                    if self._has_attachments(part):
                        return True
        return False


def main():
    """Test email fetcher."""
    from gmail_auth import GmailAuthenticator

    print("Email Fetcher Test")
    print("-" * 50)

    # Authenticate
    authenticator = GmailAuthenticator()
    service = authenticator.get_gmail_service()

    # Create fetcher
    fetcher = EmailFetcher(service)

    # Test search
    query = "is:inbox"
    emails = fetcher.search_emails(query, max_results=5)

    print(f"\nFetched {len(emails)} emails:")
    for i, email in enumerate(emails, 1):
        print(f"\n{i}. {email['subject']}")
        print(f"   From: {email['from']}")
        print(f"   Date: {email['date']}")
        print(f"   Snippet: {email['snippet'][:80]}...")


if __name__ == "__main__":
    main()

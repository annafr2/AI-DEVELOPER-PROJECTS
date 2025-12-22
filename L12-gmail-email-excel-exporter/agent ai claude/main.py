"""
MEM (Mail Excel Manager) - Main Application

Command-line interface for fetching Gmail emails and exporting to Excel.
"""

import argparse
import sys
import os
from typing import Optional

from gmail_auth import GmailAuthenticator
from email_fetcher import EmailFetcher
from excel_handler import ExcelHandler


class MEMApp:
    """Main application class for MEM."""

    def __init__(self):
        """Initialize MEM application."""
        self.authenticator = GmailAuthenticator()
        self.service = None
        self.fetcher = None

    def initialize(self) -> bool:
        """
        Initialize Gmail service and fetcher.

        Returns:
            True if successful, False otherwise
        """
        try:
            print("Initializing MEM...")
            self.service = self.authenticator.get_gmail_service()
            self.fetcher = EmailFetcher(self.service)
            print("Initialization successful!\n")
            return True
        except Exception as e:
            print(f"Initialization failed: {e}")
            return False

    def authenticate_only(self) -> bool:
        """
        Run authentication flow only.

        Returns:
            True if successful, False otherwise
        """
        try:
            print("Running authentication flow...\n")
            self.authenticator.authenticate()
            print("\nAuthentication completed successfully!")
            print("You can now use other commands to fetch and export emails.")
            return True
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False

    def fetch_and_export(
        self,
        query: str,
        max_results: int,
        output_file: Optional[str],
        output_dir: str,
        full_body: bool = False
    ) -> bool:
        """
        Fetch emails and export to Excel.

        Args:
            query: Gmail search query
            max_results: Maximum number of emails to fetch
            output_file: Output filename (optional)
            output_dir: Output directory
            full_body: Include full email body (no truncation)

        Returns:
            True if successful, False otherwise
        """
        if not self.initialize():
            return False

        try:
            # Fetch emails
            print(f"Query: '{query}'")
            print(f"Max results: {max_results}\n")

            emails = self.fetcher.search_emails(query, max_results)

            if not emails:
                print("No emails found matching your query.")
                return False

            # Export to Excel
            handler = ExcelHandler()

            if full_body:
                output_path = handler.export_emails_with_full_body(
                    emails,
                    filename=output_file,
                    output_dir=output_dir
                )
            else:
                output_path = handler.export_emails(
                    emails,
                    filename=output_file,
                    output_dir=output_dir
                )

            print(f"\nSuccess! {len(emails)} emails exported to:")
            print(f"  {output_path}")

            return True

        except Exception as e:
            print(f"Error: {e}")
            return False

    def show_profile(self) -> bool:
        """
        Display Gmail account profile information.

        Returns:
            True if successful, False otherwise
        """
        if not self.initialize():
            return False

        try:
            profile = self.service.users().getProfile(userId='me').execute()

            print("Gmail Account Profile")
            print("-" * 50)
            print(f"Email: {profile.get('emailAddress')}")
            print(f"Total Messages: {profile.get('messagesTotal')}")
            print(f"Total Threads: {profile.get('threadsTotal')}")
            print(f"History ID: {profile.get('historyId')}")

            return True

        except Exception as e:
            print(f"Error fetching profile: {e}")
            return False

    def revoke_auth(self) -> bool:
        """
        Revoke stored authentication.

        Returns:
            True if successful, False otherwise
        """
        print("Revoking stored authentication...")
        success = self.authenticator.revoke_credentials()

        if success:
            print("Authentication revoked successfully.")
            print("Run with --auth to re-authenticate.")
        else:
            print("Failed to revoke authentication.")

        return success


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='MEM (Mail Excel Manager) - Fetch Gmail emails and export to Excel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Authenticate only
  python main.py --auth

  # Fetch unread emails from specific sender
  python main.py --query "from:example@gmail.com is:unread" --max 50

  # Fetch emails with custom filename
  python main.py --query "subject:invoice" --output invoices.xlsx

  # Fetch with full email body
  python main.py --query "has:attachment" --full-body

  # Show account profile
  python main.py --profile

  # Revoke authentication
  python main.py --revoke

Gmail Query Examples:
  from:sender@example.com           - From specific sender
  to:recipient@example.com          - To specific recipient
  subject:keyword                   - Subject contains keyword
  after:2024/01/01                  - After specific date
  before:2024/12/31                 - Before specific date
  is:unread                         - Unread emails
  is:important                      - Important emails
  has:attachment                    - Has attachments
  label:work                        - Specific label
  newer_than:7d                     - Newer than 7 days
        """
    )

    # Command options
    parser.add_argument(
        '--auth',
        action='store_true',
        help='Run authentication flow only'
    )

    parser.add_argument(
        '--profile',
        action='store_true',
        help='Show Gmail account profile'
    )

    parser.add_argument(
        '--revoke',
        action='store_true',
        help='Revoke stored authentication'
    )

    # Query options
    parser.add_argument(
        '--query', '-q',
        type=str,
        help='Gmail search query (e.g., "from:example@gmail.com")'
    )

    parser.add_argument(
        '--max', '-m',
        type=int,
        default=100,
        help='Maximum number of emails to fetch (default: 100)'
    )

    # Output options
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output filename (default: auto-generated)'
    )

    parser.add_argument(
        '--output-dir', '-d',
        type=str,
        default='.',
        help='Output directory (default: current directory)'
    )

    parser.add_argument(
        '--full-body',
        action='store_true',
        help='Include full email body (no truncation)'
    )

    args = parser.parse_args()

    # Create app instance
    app = MEMApp()

    # Handle commands
    if args.auth:
        success = app.authenticate_only()
        sys.exit(0 if success else 1)

    elif args.profile:
        success = app.show_profile()
        sys.exit(0 if success else 1)

    elif args.revoke:
        success = app.revoke_auth()
        sys.exit(0 if success else 1)

    elif args.query:
        success = app.fetch_and_export(
            query=args.query,
            max_results=args.max,
            output_file=args.output,
            output_dir=args.output_dir,
            full_body=args.full_body
        )
        sys.exit(0 if success else 1)

    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()

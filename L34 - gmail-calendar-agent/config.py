"""
Configuration Management Module
Loads and validates environment variables and application settings
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration settings"""
    
    # Google API Settings
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/calendar'
    ]
    CREDENTIALS_FILE = 'credentials.json'
    TOKEN_FILE = 'token.pickle'
    
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Run Mode Settings
    RUN_MODE = os.getenv('RUN_MODE', 'once').lower()  # 'once' or 'continuous'
    SCAN_INTERVAL = int(os.getenv('SCAN_INTERVAL', '10'))  # seconds
    
    # Search Settings
    SEARCH_MODE = os.getenv('SEARCH_MODE', 'config').lower()  # 'config' or 'llm'
    SEARCH_QUERY = os.getenv('SEARCH_QUERY', 'is:unread')
    LLM_SEARCH_PROMPT = os.getenv('LLM_SEARCH_PROMPT', 
                                   'Find emails about meetings or appointments')
    
    # Calendar Settings
    CALENDAR_ID = os.getenv('CALENDAR_ID', 'primary')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        
        if not os.path.exists(cls.CREDENTIALS_FILE):
            errors.append(f"Missing {cls.CREDENTIALS_FILE} - download from Google Cloud Console")
        
        if cls.RUN_MODE not in ['once', 'continuous']:
            errors.append("RUN_MODE must be 'once' or 'continuous'")
        
        if cls.SEARCH_MODE not in ['config', 'llm']:
            errors.append("SEARCH_MODE must be 'config' or 'llm'")
        
        if cls.SEARCH_MODE == 'llm' and not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY required when SEARCH_MODE=llm")
        
        if cls.SCAN_INTERVAL < 1:
            errors.append("SCAN_INTERVAL must be at least 1 second")
        
        return errors

    @classmethod
    def display(cls):
        """Display current configuration (hide sensitive data)"""
        print("\n=== Configuration ===")
        print(f"Run Mode: {cls.RUN_MODE}")
        if cls.RUN_MODE == 'continuous':
            print(f"Scan Interval: {cls.SCAN_INTERVAL}s")
        print(f"Search Mode: {cls.SEARCH_MODE}")
        if cls.SEARCH_MODE == 'config':
            print(f"Search Query: {cls.SEARCH_QUERY}")
        else:
            print(f"LLM Prompt: {cls.LLM_SEARCH_PROMPT}")
            print(f"OpenAI API Key: {'*' * 10}{cls.OPENAI_API_KEY[-4:] if cls.OPENAI_API_KEY else 'NOT SET'}")
        print(f"Calendar: {cls.CALENDAR_ID}")
        print("=" * 25 + "\n")

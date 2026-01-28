"""
LLM Helper Module
Uses OpenAI to convert natural language to Gmail search queries
"""
from openai import OpenAI
from config import Config

def generate_gmail_query(natural_language_prompt):
    """
    Convert natural language to Gmail search query using LLM
    
    Args:
        natural_language_prompt: User's free-text search description
    
    Returns:
        str: Gmail API compatible search query
    """
    if not Config.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not configured")
    
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    system_prompt = """You are a Gmail search query generator. Convert natural language 
requests into Gmail API search queries.

Gmail search syntax:
- from:sender@email.com
- to:recipient@email.com
- subject:keyword
- label:labelname
- is:unread, is:read, is:starred
- has:attachment
- after:YYYY/MM/DD, before:YYYY/MM/DD
- newer_than:2d (2 days), older_than:1m (1 month)
- OR operator: {keyword1 OR keyword2}
- AND is implicit between terms

Examples:
"Unread emails from my boss" → "is:unread from:boss@company.com"
"Emails about meetings this week" → "subject:(meeting OR appointment) newer_than:7d"
"Important unread messages" → "is:unread is:important"

Respond with ONLY the search query, no explanations."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": natural_language_prompt}
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        query = response.choices[0].message.content.strip()
        print(f"LLM generated query: {query}")
        return query
        
    except Exception as e:
        print(f"LLM query generation failed: {e}")
        print("Falling back to basic 'is:unread' query")
        return "is:unread"

def extract_event_details(email_content):
    """
    Extract calendar event details from email using LLM
    
    Args:
        email_content: Email body text
    
    Returns:
        dict: Event details (title, description, start_time, end_time, location)
    """
    if not Config.OPENAI_API_KEY:
        return None
    
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    system_prompt = """Extract calendar event information from emails. 
Return JSON with: title, description, start_time, end_time, location.
Use ISO 8601 format for dates (YYYY-MM-DDTHH:MM:SS).
If information is missing, use null.
Return ONLY valid JSON, no explanations."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract event details:\n\n{email_content[:1000]}"}
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        import json
        event_data = json.loads(response.choices[0].message.content.strip())
        return event_data
        
    except Exception as e:
        print(f"Event extraction failed: {e}")
        return None

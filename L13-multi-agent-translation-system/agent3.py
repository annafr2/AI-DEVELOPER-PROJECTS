"""
Agent 3: Hebrew → English Translator
Receives Hebrew text, translates back to English
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class Agent3:
    def __init__(self):
        self.name = "Agent 3 (HE→EN)"
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")
        self.client = Anthropic(api_key=api_key)
        print(f"✓ {self.name} initialized")

    def translate(self, hebrew_text: str) -> str:
        """Translate Hebrew to English"""
        print(f"\n[{self.name}] Translating: {hebrew_text}")

        prompt = f"""Translate this Hebrew text to English. Return ONLY the English translation, nothing else.

Text: {hebrew_text}"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            english_text = message.content[0].text.strip()
            print(f"[{self.name}] Result: {english_text}")
            return english_text
        except Exception as e:
            print(f"[{self.name}] ERROR: {e}")
            return hebrew_text


if __name__ == "__main__":
    # Test
    agent = Agent3()
    result = agent.translate("החתול יושב על המחצלת.")
    print(f"\nTest result: {result}")

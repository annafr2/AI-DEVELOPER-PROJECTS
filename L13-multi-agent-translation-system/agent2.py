"""
Agent 2: Russian → Hebrew Translator
Receives Russian text, translates to Hebrew
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class Agent2:
    def __init__(self):
        self.name = "Agent 2 (RU→HE)"
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")
        self.client = Anthropic(api_key=api_key)
        print(f"✓ {self.name} initialized")

    def translate(self, russian_text: str) -> str:
        """Translate Russian to Hebrew"""
        print(f"\n[{self.name}] Translating: {russian_text}")

        prompt = f"""Translate this Russian text to Hebrew. Return ONLY the Hebrew translation, nothing else.

Text: {russian_text}"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            hebrew_text = message.content[0].text.strip()
            print(f"[{self.name}] Result: {hebrew_text}")
            return hebrew_text
        except Exception as e:
            print(f"[{self.name}] ERROR: {e}")
            return russian_text


if __name__ == "__main__":
    # Test
    agent = Agent2()
    result = agent.translate("Кошка сидит на коврике.")
    print(f"\nTest result: {result}")

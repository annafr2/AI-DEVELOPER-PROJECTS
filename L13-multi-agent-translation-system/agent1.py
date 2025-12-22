"""
Agent 1: English → Russian Translator
Receives English text, translates to Russian
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class Agent1:
    def __init__(self):
        self.name = "Agent 1 (EN→RU)"
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")
        self.client = Anthropic(api_key=api_key)
        print(f"✓ {self.name} initialized")

    def translate(self, english_text: str) -> str:
        """Translate English to Russian"""
        print(f"\n[{self.name}] Translating: {english_text}")

        prompt = f"""Translate this English text to Russian. Return ONLY the Russian translation, nothing else.

Text: {english_text}"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            russian_text = message.content[0].text.strip()
            print(f"[{self.name}] Result: {russian_text}")
            return russian_text
        except Exception as e:
            print(f"[{self.name}] ERROR: {e}")
            return english_text


if __name__ == "__main__":
    # Test
    agent = Agent1()
    result = agent.translate("The cat sits on the mat.")
    print(f"\nTest result: {result}")

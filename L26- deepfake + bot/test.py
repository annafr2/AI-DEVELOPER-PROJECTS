from google import genai
import os

GOOGLE_API_KEY="AIzaSyA1UDJZifQ-2tZoRjykzpRSA75OFKI8woI"
client = genai.Client(api_key=GOOGLE_API_KEY)

client = genai.Client(api_key=GOOGLE_API_KEY)

print("🔍 Available models:")
for model in client.models.list():
    print(f"  ✅ {model.name}")
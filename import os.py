import os
import openai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

print("🔑 API Key:", api_key[:10], "********")

response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Say Hello"}],
)

print("✅ GPT response:", response.choices[0].message.content)

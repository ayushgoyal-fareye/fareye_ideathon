import os
from openrouter import OpenRouter
from dotenv import load_dotenv
# Optional: Set your site URL and title for rankings on openrouter.ai

load_dotenv()
with OpenRouter(
    api_key=os.getenv("ANTHROPIC_API_KEY"), 
) as client:
    response = client.chat.send(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": "say something about trump"}]
    )
    print(response.choices[0].message.content)

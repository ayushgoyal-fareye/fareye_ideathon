import os
from openrouter import OpenRouter
from dotenv import load_dotenv

load_dotenv()

class TicketResolver:
    def __init__(self, model="openai/gpt-4o"):
        self.model = model
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

    def get_solution(self, problem_text, previous_tickets):
        # Construct the prompt using your variables
        prompt = (
            "You are an expert Technical Support Analyst. "
            "Analyze the following data and provide a structured resolution.\n\n"
            f"CONTEXT (Previous Tickets):\n{previous_tickets}\n\n"
            f"CURRENT ISSUE: {problem_text}\n\n"
            "--- OUTPUT INSTRUCTIONS ---\n"
            "1. Use Telegram-compatible Markdown (Bold for headers, Monospace for logs).\n"
            "2. Structure: \n"
            "   - 📋 *Issue Summary*: Brief description.\n"
            "   - 🔍 *Analysis*: Why is this happening?\n"
            "   - ✅ *Proposed Solution*: Bullet points of steps to take.\n"
            "   - 💡 *Confidence Score*: (0-100%).\n"
            "3. Keep it concise. Avoid 'filler' text like 'Certainly, here is your analysis'."
        )

        # Use the context manager and syntax from your snippet
        with OpenRouter(api_key=self.api_key) as client:
            response = client.chat.send(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content


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
        "Analyze the following data and provide a structured resolution based on historical patterns.\n\n"
        f"CONTEXT (Previous Tickets):\n{previous_tickets}\n\n"
        f"CURRENT ISSUE: {problem_text}\n\n"

    
        "--- OUTPUT INSTRUCTIONS ---\n"
        "1. **FORMAT FOR GOOGLE CHAT**: Use Google Chat compatible Markdown:\n"
        "   - Use *asterisks* for **bold** (Note: Google Chat uses *text* for bold, not double asterisks).\n"
        "   - Use `backticks` for `monospace` values or logs.\n"
        "   - Use standard URL strings (e.g., https://jira.com) which Google Chat will automatically turn blue/linkable.\n"
        "2. Structure your response as follows: \n"
        "   - 📋 **Issue Summary**: A brief, high-level description of the problem.\n"
        "   - 🔍 **Analysis**: Explain why this is happening. Identify recurring patterns "
        "(e.g., resource crunch, race conditions, or limit exhaustion). You MUST mention the "
        "relevant reference JIRA ID and the original Assignee (e.g., [JIRA ID: RCA-XXXX | Assignee: Name]).\n"
        "   - ✅ **Proposed Solution**: Provide bulleted technical steps to resolve the issue. "
        "Each step must include the supporting JIRA ID and the Assignee who handled it.\n"
        "   - 💡 **Confidence Score**: (0-100%) based on similarity to context.\n"
        "3. Keep it concise. Do not use any introductory filler text.\n"
        "4. Every observation in Analysis and every step in Solution MUST cite the source JIRA ID "
        "and the Assignee found in the provided context."
    )

        # Use the context manager and syntax from your snippet
        with OpenRouter(api_key=self.api_key) as client:
            response = client.chat.send(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content


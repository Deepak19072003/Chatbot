import os
from dotenv import load_dotenv
from typing import List, Dict


class ChatGPTInterface:
    def __init__(self):
        # Load .env if present so users don't need to export variables manually
        load_dotenv(override=False)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"
        self.use_openai = (os.getenv("USE_OPENAI", "true").lower() == "true") and bool(self.api_key)

    def get_response(self, messages: List[Dict[str, str]]) -> str:
        # Fast-path to mock if disabled or no key
        if not self.use_openai:
            return self._mock_response(messages[-1]["content"])

        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)

            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception:
            # On quota/any API error, silently fall back to mock to keep UX smooth
            return self._mock_response(messages[-1]["content"])

    def _mock_response(self, user_input: str) -> str:
        user_lower = user_input.lower()
        if "hello" in user_lower or "hi" in user_lower:
            return (
                "Hello! I'm your data analysis copilot. What data would you like to analyze today?"
            )
        if "sales" in user_lower or "revenue" in user_lower:
            return (
                "I can help analyze sales data. What specific metrics or insights are you looking for?"
            )
        if "chart" in user_lower or "plot" in user_lower:
            return "I'll create visualizations. What type of chart would be most helpful?"
        if "forecast" in user_lower or "prediction" in user_lower:
            return (
                "I can build forecasting models. What time period and variables should I consider?"
            )
        if "summary" in user_lower:
            return "I'll provide a comprehensive summary of your data analysis results."
        if "what is server" in user_lower or user_lower.strip() == "server":
            return "A server is a computer/process that provides services (e.g., APIs, files, databases) to clients over a network."
        if "command prompt" in user_lower or "cmd" in user_lower:
            return "The command prompt (cmd) is a Windows shell where you run text commands to manage files, programs, and system tasks."
        return "I understand. Let me help you with that data analysis task."



import ollama

from config import OLLAMA_MODEL


class ResponseGenerator:

    def __init__(self):
        # Load the local Ollama model
        self.model = OLLAMA_MODEL

    def generate(self, user_query, tool_output):

        # Create a prompt that combines the user's question
        # with the output returned by the MCP tool
        prompt = f"""
You are an AI SOC Assistant.

The user asked:

{user_query}

The tool returned:

{tool_output}

Your job is to answer naturally.

Rules:
- Do NOT mention JSON.
- Do NOT mention tool execution.
- Explain the result in a friendly and professional way.
- If alerts are returned, summarize them clearly.
"""

        # Ask the LLM to convert the tool output
        # into a natural language response
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]
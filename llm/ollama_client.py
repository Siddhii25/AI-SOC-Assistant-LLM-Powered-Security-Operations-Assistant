import ollama

from config import OLLAMA_MODEL
from llm.planner_prompt import build_planner_prompt
from llm.prompts import SYSTEM_PROMPT
from mcp_connector.registry import ToolRegistry


class OllamaClient:

    def __init__(self):
        # Load the local Ollama model
        self.model = OLLAMA_MODEL

        # Load all available MCP tools dynamically
        self.registry = ToolRegistry()
        self.registry.load_tools()

    def plan(self, conversation):
        # Get the latest list of available tools
        tools = self.registry.get_tools()
        # Build a planner prompt using the discovered tools
        planner_prompt = build_planner_prompt(tools)

        # Prepare messages for the Planner LLM
        messages = [
            {
                "role": "system",
                "content": planner_prompt
            }
        ]

        messages.extend(conversation)

        # Ask the Planner LLM to decide the next action
        response = ollama.chat(
            model=self.model,
            messages=messages
        )

        return response["message"]["content"]

    def chat(self, conversation):

        # Prepare messages for a normal conversation
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        messages.extend(conversation)

        # Generate a direct response from the LLM
        response = ollama.chat(
            model=self.model,
            messages=messages
        )

        return response["message"]["content"]
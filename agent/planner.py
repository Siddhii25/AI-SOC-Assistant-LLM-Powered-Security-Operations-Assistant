import json

from agent.executor import Executor
from agent.router import Router
from llm.ollama_client import OllamaClient
from llm.response_generator import ResponseGenerator


class Agent:

    def __init__(self):
        # Initialize all components of the AI Agent
        self.llm = OllamaClient()
        self.router = Router()
        self.executor = Executor()
        self.response_generator = ResponseGenerator()

    def run(self, conversation):
        # Ask the Planner LLM to decide what action should be taken
        raw_plan = self.llm.plan(conversation)
        # Remove markdown formatting if the LLM returns JSON inside ```json ```
        raw_plan = (
            raw_plan
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )
        # Convert planner response into a Python dictionary
        try:
            plan = json.loads(raw_plan)

        # If planner returns invalid JSON, treat it as a normal chat
        except json.JSONDecodeError:
            return self.llm.chat(conversation)

        # Decide which execution path to follow
        route = self.router.route(plan)

        # Normal conversation (no tool required)
        if route == "RESPOND":
            return self.llm.chat(conversation)

        # Planner needs more information from the user
        if route == "ASK_USER":
            return plan.get(
                "question",
                "Could you please provide more details?"
            )

        # Execute an MCP tool
        if route == "EXECUTE":

            # Execute the selected tool
            result = self.executor.execute(plan)

            # Extract readable text from the MCP response
            if hasattr(result, "content"):
                tool_output = "\n".join(
                    item.text
                    for item in result.content
                    if hasattr(item, "text")
                )
            else:
                tool_output = str(result)

            # Let the LLM convert tool output into a natural response
            return self.response_generator.generate(
                conversation[-1]["content"],
                tool_output
            )

        # Fallback if an unknown action is returned
        return "Unknown action returned by planner."
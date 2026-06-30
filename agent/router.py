class Router:

    def route(self, plan):
        # Read the action decided by the Planner
        action = plan.get("action")
        # Route to normal LLM response
        if action == "respond":
            return "RESPOND"
        # Route to MCP tool execution
        if action == "tool_call":
            return "EXECUTE"
        # Route to ask the user for additional information
        if action == "ask_user":
            return "ASK_USER"
        # Fallback for unknown planner actions
        return "UNKNOWN"
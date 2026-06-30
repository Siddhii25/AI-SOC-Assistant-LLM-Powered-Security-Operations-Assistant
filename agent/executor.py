from mcp_connector.client import MCPClient

class Executor:
    def __init__(self):
        # Initialize the MCP client for tool execution
        self.client = MCPClient()
    def execute(self, plan):
        # Extract tool name and arguments from the planner output
        tool = plan.get("tool")
        arguments = plan.get("arguments", {})
        # Execute the selected MCP tool
        result = self.client.execute_tool(
            tool,
            arguments
        )

        return result
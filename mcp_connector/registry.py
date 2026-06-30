from mcp_connector.client import MCPClient


class ToolRegistry:

    def __init__(self):

        # Initialize the MCP client
        self.client = MCPClient()

        # Store the list of available MCP tools
        self.tools = []

    def load_tools(self):

        # Fetch all available tools from the MCP server
        self.tools = self.client.list_tools()

    def get_tools(self):

        # Return the cached list of available tools
        return self.tools
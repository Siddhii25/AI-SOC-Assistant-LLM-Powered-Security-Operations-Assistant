import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from config import MCP_SERVER_PATH

class MCPClient:
    async def execute_tool_async(self, tool_name, arguments):

        # Configure the MCP server process
        server = StdioServerParameters(
            command="python",
            args=["server.py"],
            cwd=MCP_SERVER_PATH.parent,
        )

        try:
            # Start the MCP server and create a client session
            async with stdio_client(server) as (read, write):

                async with ClientSession(read, write) as session:

                    # Initialize the MCP connection
                    await session.initialize()

                    # Execute the requested tool with its arguments
                    result = await session.call_tool(
                        tool_name,
                        arguments
                    )

                    return result

        except Exception as e:
            print("\n====== MCP ERROR ======")
            print(type(e))
            print(e)
            raise

    def execute_tool(self, tool_name, arguments):

        # Run the asynchronous tool execution synchronously
        return asyncio.run(
            self.execute_tool_async(
                tool_name,
                arguments
            )
        )

    async def list_tools_async(self):

        # Configure the MCP server process
        server = StdioServerParameters(
            command="python",
            args=["server.py"],
            cwd=MCP_SERVER_PATH.parent,
        )

        try:
            # Start the MCP server and create a client session
            async with stdio_client(server) as (read, write):

                async with ClientSession(read, write) as session:

                    # Initialize the MCP connection
                    await session.initialize()

                    # Retrieve all available MCP tools
                    result = await session.list_tools()

                    return result.tools

        except Exception as e:
            print("\n====== MCP ERROR ======")
            print(type(e))
            print(e)
            raise

    def list_tools(self):

        # Run asynchronous tool discovery synchronously
        return asyncio.run(
            self.list_tools_async()
        )
from mcp.server.fastmcp import FastMCP

from ..client import api_call, get_client


def register(mcp: FastMCP):
    @mcp.tool()
    async def testy_system(action: str) -> str:
        """System information and diagnostics.

        Actions:
          - statistics: Get system-wide statistics (total projects, cases, etc.)
          - messages: Get system messages/announcements
          - whoami: Get current authenticated user info
        """
        client = get_client()
        if action == "statistics":
            return await api_call(client.get("system/statistics/"))
        elif action == "messages":
            return await api_call(client.get("system/messages/"))
        elif action == "whoami":
            return await api_call(client.get("users/me/"))
        else:
            return f'{{"error": "Unknown action: {action}"}}'

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ..client import api_call, get_client


def register(mcp: FastMCP):
    @mcp.tool()
    async def testy_comments(
        action: str,
        comment_id: int | None = None,
        data: dict | None = None,
        params: dict | None = None,
    ) -> str:
        """Manage comments on any entity.

        Actions:
          - list: List comments. params: {object_id, model (e.g. "testresult", "testcase"), page, page_size}
          - get: Get comment by ID. Requires comment_id
          - create: Create comment. data: {text, object_id, model}
          - update: Update comment. Requires comment_id + data: {text}
          - delete: Delete comment. Requires comment_id
        """
        client = get_client()

        if action == "list":
            return await api_call(client.get_paginated("comments/", params=params))
        elif action == "get":
            return await api_call(client.get(f"comments/{comment_id}/"))
        elif action == "create":
            return await api_call(client.post("comments/", data=data))
        elif action == "update":
            return await api_call(client.patch(f"comments/{comment_id}/", data=data))
        elif action == "delete":
            return await api_call(client.delete(f"comments/{comment_id}/"))
        else:
            return f'{{"error": "Unknown action: {action}"}}'

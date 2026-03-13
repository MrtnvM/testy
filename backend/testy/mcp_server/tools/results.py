from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ..client import api_call, get_client


def register(mcp: FastMCP):
    @mcp.tool()
    async def testy_results(
        action: str,
        result_id: int | None = None,
        data: dict | None = None,
        params: dict | None = None,
    ) -> str:
        """Manage test results.

        Actions:
          - list: List results. params: {test, status, page, page_size}
          - get: Get result by ID. Requires result_id
          - create: Create result. data: {test, status, comment?, elapsed?}
          - update: Update result. Requires result_id + data
          - delete: Delete result. Requires result_id
        """
        client = get_client()

        if action == "list":
            return await api_call(client.get_paginated("results/", params=params))
        elif action == "get":
            return await api_call(client.get(f"results/{result_id}/"))
        elif action == "create":
            return await api_call(client.post("results/", data=data))
        elif action == "update":
            return await api_call(client.patch(f"results/{result_id}/", data=data))
        elif action == "delete":
            return await api_call(client.delete(f"results/{result_id}/"))
        else:
            return f'{{"error": "Unknown action: {action}"}}'

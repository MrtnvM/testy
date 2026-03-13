from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ..client import api_call, get_client


def register(mcp: FastMCP):
    @mcp.tool()
    async def testy_tests(
        action: str,
        test_id: int | None = None,
        data: dict | None = None,
        params: dict | None = None,
    ) -> str:
        """Manage test instances (test case + test plan binding).

        Actions:
          - list: List tests. params: {testplan, case, assignee, status_id, search, page, page_size}
          - get: Get test by ID. Requires test_id
          - create: Create test. data: {case, testplan, assignee?, status?}
          - update: Update test. Requires test_id + data
          - delete: Delete test. Requires test_id
          - results_union: Get test results + comments. Requires test_id
        """
        client = get_client()

        if action == "list":
            return await api_call(client.get_paginated("tests/", params=params))
        elif action == "get":
            return await api_call(client.get(f"tests/{test_id}/"))
        elif action == "create":
            return await api_call(client.post("tests/", data=data))
        elif action == "update":
            return await api_call(client.patch(f"tests/{test_id}/", data=data))
        elif action == "delete":
            return await api_call(client.delete(f"tests/{test_id}/"))
        elif action == "results_union":
            return await api_call(client.get_paginated(f"tests/{test_id}/results-union/", params=params))
        else:
            return f'{{"error": "Unknown action: {action}"}}'

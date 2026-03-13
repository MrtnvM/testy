from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ..client import api_call, get_client


def register(mcp: FastMCP):
    @mcp.tool()
    async def testy_cases(
        action: str,
        case_id: int | None = None,
        data: dict | None = None,
        params: dict | None = None,
    ) -> str:
        """Manage test cases.

        Actions:
          - list: List cases. params: {project, suite, search, is_archive, labels, page, page_size}
          - get: Get case by ID. Requires case_id
          - create: Create case. data: {name, suite, project, description?, priority?, labels?, steps?}
          - update: Update case. Requires case_id + data
          - delete: Delete case. Requires case_id
          - history: Get case change history. Requires case_id
          - search: Search cases. params: {project, search}
          - copy: Copy cases. data: {ids, project, suite?}
          - tests: Get tests created from case. Requires case_id
        """
        client = get_client()

        if action == "list":
            return await api_call(client.get_paginated("cases/", params=params))
        elif action == "get":
            return await api_call(client.get(f"cases/{case_id}/"))
        elif action == "create":
            return await api_call(client.post("cases/", data=data))
        elif action == "update":
            return await api_call(client.patch(f"cases/{case_id}/", data=data))
        elif action == "delete":
            return await api_call(client.delete(f"cases/{case_id}/"))
        elif action == "history":
            return await api_call(client.get_paginated(f"cases/{case_id}/history/", params=params))
        elif action == "search":
            return await api_call(client.get_paginated("cases/", params=params))
        elif action == "copy":
            return await api_call(client.post("cases/copy/", data=data))
        elif action == "tests":
            return await api_call(client.get_paginated(f"cases/{case_id}/tests/", params=params))
        else:
            return f'{{"error": "Unknown action: {action}"}}'

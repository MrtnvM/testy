from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ..client import api_call, get_client


def register(mcp: FastMCP):
    @mcp.tool()
    async def testy_suites(
        action: str,
        suite_id: int | None = None,
        data: dict | None = None,
        params: dict | None = None,
    ) -> str:
        """Manage test suites (hierarchical).

        Actions:
          - list: List suites. params: {project, search, is_archive, parent, page, page_size}
          - get: Get suite by ID. Requires suite_id
          - create: Create suite. data: {name, project, parent?, description?}
          - update: Update suite. Requires suite_id + data
          - delete: Delete suite. Requires suite_id
          - cases: Get cases in suite. Requires suite_id. params: {search, page, page_size}
          - descendants: Get descendant tree. Requires suite_id
          - breadcrumbs: Get breadcrumb path. Requires suite_id
          - copy: Copy suites. data: {ids, project, parent?}
          - search: Search suites. params: {project, search}
        """
        client = get_client()

        if action == "list":
            return await api_call(client.get_paginated("suites/", params=params))
        elif action == "get":
            return await api_call(client.get(f"suites/{suite_id}/"))
        elif action == "create":
            return await api_call(client.post("suites/", data=data))
        elif action == "update":
            return await api_call(client.patch(f"suites/{suite_id}/", data=data))
        elif action == "delete":
            return await api_call(client.delete(f"suites/{suite_id}/"))
        elif action == "cases":
            return await api_call(client.get_paginated(f"suites/{suite_id}/cases/", params=params))
        elif action == "descendants":
            return await api_call(client.get(f"suites/{suite_id}/descendants-tree/"))
        elif action == "breadcrumbs":
            return await api_call(client.get(f"suites/{suite_id}/breadcrumbs/"))
        elif action == "copy":
            return await api_call(client.post("suites/copy/", data=data))
        elif action == "search":
            return await api_call(client.get_paginated("suites/", params=params))
        else:
            return f'{{"error": "Unknown action: {action}"}}'

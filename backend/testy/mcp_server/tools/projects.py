from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ..client import api_call, get_client


def register(mcp: FastMCP):
    @mcp.tool()
    async def testy_projects(
        action: str,
        project_id: int | None = None,
        data: dict | None = None,
        params: dict | None = None,
    ) -> str:
        """Manage Testy projects.

        Actions:
          - list: List projects. params: {search, is_archive, page, page_size}
          - get: Get project by ID. Requires project_id
          - create: Create project. data: {name, description?, is_archive?}
          - update: Update project. Requires project_id + data
          - delete: Delete (archive) project. Requires project_id
          - members: Get project members. Requires project_id
          - statistics: Get project statistics. Requires project_id
          - progress: Get project progress. Requires project_id
          - testplans: Get project test plans. Requires project_id
          - parameters: Get project parameters. Requires project_id
        """
        client = get_client()

        if action == "list":
            return await api_call(client.get_paginated("projects/", params=params))
        elif action == "get":
            return await api_call(client.get(f"projects/{project_id}/"))
        elif action == "create":
            return await api_call(client.post("projects/", data=data))
        elif action == "update":
            return await api_call(client.patch(f"projects/{project_id}/", data=data))
        elif action == "delete":
            return await api_call(client.delete(f"projects/{project_id}/"))
        elif action == "members":
            return await api_call(client.get(f"projects/{project_id}/members/"))
        elif action == "statistics":
            return await api_call(client.get(f"projects/{project_id}/statistics/"))
        elif action == "progress":
            return await api_call(client.get(f"projects/{project_id}/progress/"))
        elif action == "testplans":
            return await api_call(client.get_paginated(f"projects/{project_id}/testplans/", params=params))
        elif action == "parameters":
            return await api_call(client.get_paginated(f"projects/{project_id}/parameters/", params=params))
        else:
            return f'{{"error": "Unknown action: {action}"}}'

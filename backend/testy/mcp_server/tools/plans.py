from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ..client import api_call, get_client


def register(mcp: FastMCP):
    @mcp.tool()
    async def testy_plans(
        action: str,
        plan_id: int | None = None,
        data: dict | None = None,
        params: dict | None = None,
    ) -> str:
        """Manage test plans (hierarchical).

        Actions:
          - list: List plans. params: {project, search, is_archive, parent, page, page_size}
          - get: Get plan by ID. Requires plan_id
          - create: Create plan. data: {name, project, parent?, description?, started_at?, due_date?}
          - update: Update plan. Requires plan_id + data
          - delete: Delete plan. Requires plan_id
          - statistics: Get plan statistics (pie chart). Requires plan_id
          - histogram: Get plan histogram data. Requires plan_id
          - progress: Get plan progress metrics. Requires plan_id
          - activity: Get plan activity log. Requires plan_id
          - cases: Get cases in plan. Requires plan_id
          - tests: Get tests in plan. Requires plan_id. params: {search, status_id, assignee, page, page_size}
          - copy: Copy plans. data: {ids, project, parent?}
          - descendants: Get descendant tree. Requires plan_id
          - breadcrumbs: Get breadcrumb path. Requires plan_id
          - suites: Get suites in plan. Requires plan_id
        """
        client = get_client()

        if action == "list":
            return await api_call(client.get_paginated("testplans/", params=params))
        elif action == "get":
            return await api_call(client.get(f"testplans/{plan_id}/"))
        elif action == "create":
            return await api_call(client.post("testplans/", data=data))
        elif action == "update":
            return await api_call(client.patch(f"testplans/{plan_id}/", data=data))
        elif action == "delete":
            return await api_call(client.delete(f"testplans/{plan_id}/"))
        elif action == "statistics":
            return await api_call(client.get(f"testplans/{plan_id}/statistics/"))
        elif action == "histogram":
            return await api_call(client.get(f"testplans/{plan_id}/histogram/"))
        elif action == "progress":
            return await api_call(client.get(f"testplans/{plan_id}/progress/"))
        elif action == "activity":
            return await api_call(client.get_paginated(f"testplans/{plan_id}/activity/", params=params))
        elif action == "cases":
            return await api_call(client.get_paginated(f"testplans/{plan_id}/cases/", params=params))
        elif action == "tests":
            return await api_call(client.get_paginated(f"testplans/{plan_id}/tests/", params=params))
        elif action == "copy":
            return await api_call(client.post("testplans/copy/", data=data))
        elif action == "descendants":
            return await api_call(client.get(f"testplans/{plan_id}/descendants-tree/"))
        elif action == "breadcrumbs":
            return await api_call(client.get(f"testplans/{plan_id}/breadcrumbs/"))
        elif action == "suites":
            return await api_call(client.get_paginated(f"testplans/{plan_id}/suites/", params=params))
        else:
            return f'{{"error": "Unknown action: {action}"}}'

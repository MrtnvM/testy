from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ..client import api_call, get_client


def register(mcp: FastMCP):
    @mcp.tool()
    async def testy_users(
        action: str,
        user_id: int | None = None,
        role_id: int | None = None,
        data: dict | None = None,
        params: dict | None = None,
    ) -> str:
        """Manage users, roles, and groups.

        Actions:
          - list: List users. params: {search, page, page_size}
          - get: Get user by ID. Requires user_id
          - me: Get current authenticated user
          - create: Create user. data: {username, email, password, first_name?, last_name?}
          - update: Update user. Requires user_id + data
          - delete: Delete user. Requires user_id
          - roles: List all roles
          - role_assign: Assign role. data: {user, project, role}
          - role_unassign: Unassign role. data: {user, project, role}
          - permissions: List all available permissions
          - groups: List groups. params: {search, page, page_size}
        """
        client = get_client()

        if action == "list":
            return await api_call(client.get_paginated("users/", params=params))
        elif action == "get":
            return await api_call(client.get(f"users/{user_id}/"))
        elif action == "me":
            return await api_call(client.get("users/me/"))
        elif action == "create":
            return await api_call(client.post("users/", data=data))
        elif action == "update":
            return await api_call(client.patch(f"users/{user_id}/", data=data))
        elif action == "delete":
            return await api_call(client.delete(f"users/{user_id}/"))
        elif action == "roles":
            return await api_call(client.get_paginated("roles/", params=params))
        elif action == "role_assign":
            return await api_call(client.post("roles/assign/", data=data))
        elif action == "role_unassign":
            return await api_call(client.post("roles/unassign/", data=data))
        elif action == "permissions":
            return await api_call(client.get("roles/permissions/"))
        elif action == "groups":
            return await api_call(client.get_paginated("groups/", params=params))
        else:
            return f'{{"error": "Unknown action: {action}"}}'

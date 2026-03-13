from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ..client import api_call, get_client


def register(mcp: FastMCP):
    @mcp.tool()
    async def testy_metadata(
        action: str,
        item_id: int | None = None,
        data: dict | None = None,
        params: dict | None = None,
    ) -> str:
        """Manage labels, parameters, result statuses, and custom attributes.

        Actions:
          Labels:
            - labels_list: List labels. params: {project, search, page, page_size}
            - label_get: Get label by ID. Requires item_id
            - label_create: Create label. data: {name, color?, project}
            - label_update: Update label. Requires item_id + data
            - label_delete: Delete label. Requires item_id

          Parameters:
            - params_list: List parameters. params: {project, page, page_size}
            - param_create: Create parameter. data: {title, project, group_name?}
            - param_update: Update parameter. Requires item_id + data
            - param_delete: Delete parameter. Requires item_id

          Result Statuses:
            - statuses_list: List result statuses. params: {project, page, page_size}
            - status_create: Create status. data: {name, project, color?}
            - status_update: Update status. Requires item_id + data
            - status_delete: Delete status. Requires item_id

          Custom Attributes:
            - custom_attrs_list: List custom attributes. params: {project, page, page_size}
            - custom_attr_create: Create attribute. data: {name, project, type?, options?}
            - custom_attr_update: Update attribute. Requires item_id + data
            - custom_attr_delete: Delete attribute. Requires item_id
        """
        client = get_client()

        # Labels
        if action == "labels_list":
            return await api_call(client.get_paginated("labels/", params=params))
        elif action == "label_get":
            return await api_call(client.get(f"labels/{item_id}/"))
        elif action == "label_create":
            return await api_call(client.post("labels/", data=data))
        elif action == "label_update":
            return await api_call(client.patch(f"labels/{item_id}/", data=data))
        elif action == "label_delete":
            return await api_call(client.delete(f"labels/{item_id}/"))

        # Parameters
        elif action == "params_list":
            return await api_call(client.get_paginated("parameters/", params=params))
        elif action == "param_create":
            return await api_call(client.post("parameters/", data=data))
        elif action == "param_update":
            return await api_call(client.patch(f"parameters/{item_id}/", data=data))
        elif action == "param_delete":
            return await api_call(client.delete(f"parameters/{item_id}/"))

        # Result Statuses
        elif action == "statuses_list":
            return await api_call(client.get_paginated("statuses/", params=params))
        elif action == "status_create":
            return await api_call(client.post("statuses/", data=data))
        elif action == "status_update":
            return await api_call(client.patch(f"statuses/{item_id}/", data=data))
        elif action == "status_delete":
            return await api_call(client.delete(f"statuses/{item_id}/"))

        # Custom Attributes
        elif action == "custom_attrs_list":
            return await api_call(client.get_paginated("custom-attributes/", params=params))
        elif action == "custom_attr_create":
            return await api_call(client.post("custom-attributes/", data=data))
        elif action == "custom_attr_update":
            return await api_call(client.patch(f"custom-attributes/{item_id}/", data=data))
        elif action == "custom_attr_delete":
            return await api_call(client.delete(f"custom-attributes/{item_id}/"))

        else:
            return f'{{"error": "Unknown action: {action}"}}'

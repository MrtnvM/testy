from __future__ import annotations

import json

import httpx

from .config import get_config

_client: TestyClient | None = None


class TestyClient:
    def __init__(self, url: str, token: str, page_size: int = 100):
        self._base = f"{url}/api/v2/"
        self._page_size = page_size
        self._http = httpx.AsyncClient(
            base_url=self._base,
            headers={"Authorization": f"Token {token}"},
            timeout=30.0,
        )

    async def get(self, path: str, params: dict | None = None) -> dict | list:
        r = await self._http.get(path, params=params)
        r.raise_for_status()
        return r.json()

    async def get_paginated(
        self,
        path: str,
        params: dict | None = None,
        max_pages: int = 10,
    ) -> dict:
        params = dict(params or {})
        params.setdefault("page_size", self._page_size)

        all_results: list = []
        page = 1
        total_count = 0

        while page <= max_pages:
            params["page"] = page
            r = await self._http.get(path, params=params)
            r.raise_for_status()
            data = r.json()

            if isinstance(data, list):
                return {"results": data, "count": len(data)}

            all_results.extend(data.get("results", []))
            total_count = data.get("count", len(all_results))

            pages_info = data.get("pages", {})
            if not pages_info.get("next"):
                break
            page += 1

        return {"results": all_results, "count": total_count}

    async def post(self, path: str, data: dict | list | None = None) -> dict | list:
        r = await self._http.post(path, json=data)
        r.raise_for_status()
        if r.status_code == 204:
            return {"ok": True}
        return r.json()

    async def put(self, path: str, data: dict | None = None) -> dict:
        r = await self._http.put(path, json=data)
        r.raise_for_status()
        return r.json()

    async def patch(self, path: str, data: dict | None = None) -> dict:
        r = await self._http.patch(path, json=data)
        r.raise_for_status()
        return r.json()

    async def delete(self, path: str, params: dict | None = None) -> dict:
        r = await self._http.delete(path, params=params)
        r.raise_for_status()
        if r.status_code == 204:
            return {"ok": True}
        try:
            return r.json()
        except Exception:
            return {"ok": True}


def get_client() -> TestyClient:
    global _client
    if _client is None:
        cfg = get_config()
        _client = TestyClient(cfg["url"], cfg["token"], cfg["page_size"])
    return _client


async def api_call(coro):
    """Wrap an API coroutine, returning JSON string with error handling."""
    try:
        result = await coro
        return json.dumps(result, ensure_ascii=False, default=str)
    except httpx.HTTPStatusError as e:
        body = e.response.text
        try:
            detail = json.loads(body)
        except Exception:
            detail = body
        return json.dumps(
            {"error": str(e), "status_code": e.response.status_code, "detail": detail},
            ensure_ascii=False,
            default=str,
        )
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, default=str)

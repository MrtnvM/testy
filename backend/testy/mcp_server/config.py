import os


def get_config() -> dict:
    url = os.environ.get("TESTY_URL")
    token = os.environ.get("TESTY_TOKEN")
    if not url:
        raise RuntimeError("TESTY_URL environment variable is required")
    if not token:
        raise RuntimeError("TESTY_TOKEN environment variable is required")
    return {
        "url": url.rstrip("/"),
        "token": token,
        "page_size": int(os.environ.get("TESTY_PAGE_SIZE", "100")),
    }

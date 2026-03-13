import os

from mcp.server.fastmcp import FastMCP

from .tools import cases, comments, metadata, plans, projects, results, suites, system, tests, users

mcp = FastMCP(
    "testy",
    instructions=(
        "Testy TMS MCP server. Provides CRUD access to Testy Test Management System "
        "via its REST API v2. Use testy_system with action 'whoami' to verify connectivity. "
        "All list actions support pagination via params: {page, page_size}. "
        "Most entities belong to a project — pass project ID in params or data as needed."
    ),
    host=os.environ.get("MCP_HOST", "0.0.0.0"),
    port=int(os.environ.get("MCP_PORT", "8080")),
)

# Register all tool modules
system.register(mcp)
projects.register(mcp)
suites.register(mcp)
cases.register(mcp)
plans.register(mcp)
tests.register(mcp)
results.register(mcp)
users.register(mcp)
comments.register(mcp)
metadata.register(mcp)

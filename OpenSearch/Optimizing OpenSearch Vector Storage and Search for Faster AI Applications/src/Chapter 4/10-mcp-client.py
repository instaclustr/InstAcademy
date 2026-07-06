"""Chapter 4 · Lesson 4-4 — connect to the built-in OpenSearch MCP server as an external client.

Prerequisites:
    1. OpenSearch 3.3+ with the MCP server enabled:
         PUT _cluster/settings { "persistent": { "plugins.ml_commons.mcp_server_enabled": "true" } }
    2. Tools registered (POST /_plugins/_ml/mcp/tools/_register).
    3. pip install fastmcp

Any MCP-compatible client (LangChain, Claude Desktop, Cursor) can connect to the same
Streamable HTTP endpoint at /_plugins/_ml/mcp and reuse the indexes and pipelines built
in this chapter. Set the URL/credentials for your cluster before running.
"""

import asyncio
import os

# Point at your cluster's MCP endpoint. For a secured cluster include auth per the
# fastmcp / httpx transport options; localhost dev clusters may use plain HTTP.
MCP_URL = os.getenv("OPENSEARCH_MCP_URL", "http://localhost:9200/_plugins/_ml/mcp")


async def main():
    try:
        from fastmcp import Client
    except ImportError:
        raise SystemExit("pip install fastmcp to run this example.")

    async with Client(MCP_URL) as client:
        # Discover the tools the server exposes.
        for tool in await client.list_tools():
            print("tool:", tool.name)

        # Call a tool: list indexes, then search the bookstore.
        print(await client.call_tool("ListIndexTool", {}))
        result = await client.call_tool(
            "SearchIndexTool",
            {"index": "bookstore-rag", "query": '{"match": {"content": "mystery"}}'},
        )
        print("search result:", result)


if __name__ == "__main__":
    asyncio.run(main())

import os
import asyncio

# Set up environment BEFORE importing dbt_mcp
os.environ["DISABLE_SEMANTIC_LAYER"] = "true"
os.environ["DISABLE_DISCOVERY"] = "true"
os.environ["DISABLE_REMOTE"] = "true"
os.environ["DBT_PROJECT_DIR"] = "."

from dbt_mcp.mcp.server import dbt_mcp

async def test_tools():
    print("--- Listing Registered MCP Tools ---")
    tools = await dbt_mcp.list_tools()
    for tool in tools:
        print(f"- {tool.name}: {tool.description[:60]}...")

    print("\n--- Executing 'list' Tool ---")
    result = await dbt_mcp.call_tool("list", {})
    if result and hasattr(result[0], 'text'):
        print(f"Result (first 500 chars):\n{result[0].text[:500]}")
    else:
        print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(test_tools())

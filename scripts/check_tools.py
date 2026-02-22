
import asyncio
import os

# Set defaults BEFORE importing dbt_mcp
os.environ["DISABLE_SEMANTIC_LAYER"] = "true"
os.environ["DISABLE_DISCOVERY"] = "true"
os.environ["DISABLE_REMOTE"] = "true"
os.environ["DBT_PROJECT_DIR"] = "."
os.environ["DBT_PROFILES_DIR"] = "."

from dbt_mcp.mcp.server import dbt_mcp

async def main():
    tools = await dbt_mcp.list_tools()
    for tool in tools:
        print(f"Tool: {tool.name}")
        print(f"Description: {tool.description}")
        print(f"Input Schema: {tool.inputSchema}")
        print("-" * 20)

if __name__ == "__main__":
    asyncio.run(main())

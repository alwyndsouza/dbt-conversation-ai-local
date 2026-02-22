#!/usr/bin/env python3
"""Check all available dbt-mcp tools."""
import os
os.environ["DISABLE_SEMANTIC_LAYER"] = "true"
os.environ["DISABLE_DISCOVERY"] = "true"
os.environ["DISABLE_REMOTE"] = "true"
os.environ["DBT_PROJECT_DIR"] = "."
os.environ["DBT_PROFILES_DIR"] = "."

import asyncio
from dbt_mcp.mcp.server import dbt_mcp

async def main():
    tools = await dbt_mcp.list_tools()
    print("=== dbt-mcp Built-in Tools ===")
    for t in tools:
        print(f"  {t.name}")
    print(f"\nTotal: {len(tools)} tools")

asyncio.run(main())

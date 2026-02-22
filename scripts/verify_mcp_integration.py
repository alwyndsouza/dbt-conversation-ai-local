import os
import asyncio
from dotenv import load_dotenv

def test_integration():
    # Load .env
    load_dotenv()

    print("--- Environment Variables ---")
    vars_to_check = [
        "DISABLE_SEMANTIC_LAYER",
        "DISABLE_DISCOVERY",
        "DISABLE_REMOTE",
        "DBT_PROJECT_DIR",
        "DBT_PROFILES_DIR"
    ]
    for var in vars_to_check:
        print(f"{var}: {os.environ.get(var)}")

    # Import dbt-mcp
    try:
        from dbt_mcp.mcp.server import dbt_mcp
        print("\ndbt-mcp imported successfully.")

        # List tools
        tools = asyncio.run(dbt_mcp.list_tools())
        print(f"Available tools: {[t.name for t in tools]}")

        if len(tools) > 0:
            print("SUCCESS: dbt-mcp is integrated and tools are available.")
        else:
            print("WARNING: No tools found. Check if dbt project is correctly located.")

    except Exception as e:
        print(f"\nFAILURE: could not initialize dbt-mcp: {e}")

if __name__ == "__main__":
    test_integration()


import asyncio
import os
import sys

# Set defaults
os.environ["DISABLE_SEMANTIC_LAYER"] = "true"
os.environ["DISABLE_DISCOVERY"] = "true"
os.environ["DISABLE_REMOTE"] = "true"
os.environ["DBT_PROJECT_DIR"] = "."
os.environ["DBT_PROFILES_DIR"] = "."

# Mock streamlit to avoid errors on import
from unittest.mock import MagicMock
sys.modules["streamlit"] = MagicMock()

# Mock ollama to avoid network calls or hangs on import of streamlit_app
mock_ollama = MagicMock()
mock_ollama.list.return_value = []
sys.modules["ollama"] = mock_ollama
import streamlit_app

async def main():
    tools = await streamlit_app.get_tools_definitions()
    for tool in tools:
        print(f"Tool: {tool['function']['name']}")

if __name__ == "__main__":
    asyncio.run(main())

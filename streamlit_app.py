import streamlit as st
import ollama
import asyncio
import os
import json
import subprocess
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set defaults if not provided in .env
os.environ.setdefault("DISABLE_SEMANTIC_LAYER", "true")
os.environ.setdefault("DISABLE_DISCOVERY", "true")
os.environ.setdefault("DISABLE_REMOTE", "true")
os.environ.setdefault("DBT_PROJECT_DIR", ".")
os.environ.setdefault("DBT_PROFILES_DIR", ".")

# Import dbt-mcp after setting environment variables
from dbt_mcp.mcp.server import dbt_mcp

# --- Tool Registration ---

# Register MetricFlow tools for local MetricFlow if mf is available
def register_mf_tools():
    try:
        subprocess.run(["mf", "--version"], capture_output=True, check=True)

        # Only register if not already registered to avoid warnings in Streamlit logs
        try:
            # We use a simple check for one of our tools
            async def check_registered():
                tools = await dbt_mcp.list_tools()
                return any(t.name == "metricflow_list_metrics" for t in tools)
            if asyncio.run(check_registered()):
                return
        except Exception:
            pass

        @dbt_mcp.tool()
        async def metricflow_list_metrics():
            """List all available metrics in the dbt semantic layer using MetricFlow CLI."""
            try:
                result = subprocess.run(["mf", "list", "metrics"], capture_output=True, text=True, check=True)
                return result.stdout
            except subprocess.CalledProcessError as e:
                return f"Error: {e.stderr}"

        @dbt_mcp.tool()
        async def metricflow_list_dimensions(metrics: list[str] = None):
            """List available dimensions for all or specific metrics.
            Args:
                metrics: Optional list of metric names to show dimensions for.
            """
            # Handle potential string inputs if LLM doesn't follow schema strictly
            if isinstance(metrics, str): metrics = [metrics]

            cmd = ["mf", "list", "dimensions"]
            if metrics:
                cmd.extend(["--metrics", ",".join(metrics)])
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                return result.stdout
            except subprocess.CalledProcessError as e:
                return f"Error: {e.stderr}"

        @dbt_mcp.tool()
        async def metricflow_list_semantic_models():
            """List all semantic models in the dbt project."""
            try:
                result = subprocess.run(["mf", "list", "semantic-models"], capture_output=True, text=True, check=True)
                return result.stdout
            except subprocess.CalledProcessError as e:
                return f"Error: {e.stderr}"

        @dbt_mcp.tool()
        async def metricflow_query(metrics: list[str], group_by: list[str] = None, where: str = None, limit: int = None):
            """Execute a dbt semantic layer query using MetricFlow CLI.
            Args:
                metrics: List of metric names to query.
                group_by: List of dimensions to group by (e.g., ['metric_time', 'customer__state']).
                where: Filter expression (SQL-like, e.g., "customer__state = 'CA'").
                limit: Limit the number of rows returned.
            """
            # Handle potential string inputs if LLM doesn't follow schema strictly
            if isinstance(metrics, str): metrics = [metrics]
            if isinstance(group_by, str): group_by = [group_by]

            cmd = ["mf", "query", "--metrics", ",".join(metrics)]
            if group_by: cmd.extend(["--group-by", ",".join(group_by)])
            if where: cmd.extend(["--where", where])
            if limit is not None:
                try:
                    limit_value = int(limit)
                except (TypeError, ValueError):
                    return "Error: 'limit' must be an integer."
                if limit_value <= 0:
                    return "Error: 'limit' must be a positive integer."
                cmd.extend(["--limit", str(limit_value)])

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                return result.stdout
            except subprocess.CalledProcessError as e:
                return f"Error: {e.stderr}\n{e.stdout}"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

register_mf_tools()

# --- Helper Functions ---

def clean_dbt_output(text: str) -> str:
    """Filter out noisy dbt JSON log lines and ANSI escape codes."""
    if not text:
        return ""

    # Remove ANSI escape codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    text = ansi_escape.sub('', text)

    lines = text.split('\n')
    clean_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip dbt JSON log lines
        if line.startswith('{') and '"info"' in line and '"code"' in line:
            continue
        clean_lines.append(line)

    return '\n'.join(clean_lines)

async def get_tools_definitions():
    """Get MCP tools and convert them to Ollama tool format."""
    mcp_tools = await dbt_mcp.list_tools()
    ollama_tools = []
    for tool in mcp_tools:
        ollama_tools.append({
            'type': 'function',
            'function': {
                'name': tool.name,
                'description': tool.description,
                'parameters': tool.inputSchema
            }
        })
    return ollama_tools

# --- Streamlit UI ---

st.set_page_config(page_title="Conversational Data Experience", page_icon="🤖", layout="wide")

# Custom CSS to match the clean look of the screenshot
st.markdown("""
    <style>
    .stChatMessage {
        background-color: transparent !important;
    }
    .stStatusWidget {
        border: none !important;
        background-color: #f0f2f6 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Conversational Data Experience")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    try:
        response = ollama.list()
        models = [m['model'] if 'model' in m else m['name'] for m in response.get('models', [])]
        selected_model = st.selectbox("LLM Model", models) if models else None
        if not models:
            st.warning("No Ollama models found. Run `ollama pull llama3.2`.")
    except Exception as e:
        st.error(f"Ollama connection error: {e}")
        selected_model = None

    st.divider()
    st.markdown("### Environment Variables")
    st.code(f"DBT_PROJECT_DIR: {os.environ.get('DBT_PROJECT_DIR')}\nDBT_PROFILES_DIR: {os.environ.get('DBT_PROFILES_DIR')}")

    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("### Examples")
    examples = [
        "Show me all the metrics that are defined",
        "What are the dimensions for total_revenue?",
        "Show total revenue by state",
        "What is my Churn Rate and which is the best performing state. How can I increase my revenue and decrease churn. Please provide me with actionable insights"

    ]
    for example in examples:
        if st.button(example):
            st.session_state.example_prompt = example

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"] and message.get("content"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat Input
prompt = st.chat_input("How can I help you with your dbt project today?")

# Handle example prompt
if "example_prompt" in st.session_state:
    prompt = st.session_state.example_prompt
    del st.session_state.example_prompt

if prompt:
    if not selected_model:
        st.error("Please select a valid Ollama model in the sidebar before chatting.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        # Fetch tools once
        available_tools = asyncio.run(get_tools_definitions())

        system_message = {
            "role": "system",
            "content": (
                "You are an expert dbt analytics engineer. You have access to tools that can "
                "interact with a dbt project and its semantic layer.\n\n"
                "When asked a question:\n"
                "1. **Discovery**: If you need information about models, use 'list'. "
                "If you need information about metrics, dimensions, or semantic models, use 'metricflow_list_metrics', "
                "'metricflow_list_dimensions', or 'metricflow_list_semantic_models'.\n"
                "2. **Querying**: If asked for metric data, use 'metricflow_query'. Always try to discover "
                "available metrics and dimensions first if you are unsure of the exact names.\n"
                "3. **SQL**: If you need to query the underlying data directly (not via metrics), use 'show'.\n"
                "4. **Execution**: If asked to build or test the project, use 'run', 'test', or 'build'.\n\n"
                "Be conversational and explain what you are doing, just like in the Claude Desktop interface. "
                "If a tool returns an error, try to understand why and correct your approach (e.g., by listing available resources)."
            )
        }

        # Interaction loop
        messages = [system_message] + st.session_state.messages

        # Limit iterations to prevent infinite loops
        for _ in range(5):
            try:
                response = ollama.chat(
                    model=selected_model,
                    messages=messages,
                    tools=available_tools
                )
            except Exception as e:
                st.error(f"Ollama Error: {e}")
                break

            msg = response['message']

            # If the LLM produces content before or instead of tool calls
            if msg.get('content'):
                st.markdown(msg['content'])

            if not msg.get('tool_calls'):
                # Final response reached
                if msg.get('content'):
                    st.session_state.messages.append({"role": "assistant", "content": msg['content']})
                break

            # Handle tool calls
            messages.append(msg)
            # CRITICAL: Also append to session state so it's persisted
            st.session_state.messages.append(msg)

            for tool_call in msg['tool_calls']:
                tool_name = tool_call['function']['name']
                tool_args = tool_call['function']['arguments']

                # Show status widget like in the Claude screenshot
                with st.status(f"Used dbt-mcp integration", expanded=False) as status:
                    st.write(f"Calling `{tool_name}` with arguments: `{tool_args}`")
                    try:
                        output_obj = asyncio.run(dbt_mcp.call_tool(tool_name, tool_args))

                        # Handle different output formats from mcp tools
                        if isinstance(output_obj, list) and len(output_obj) > 0 and hasattr(output_obj[0], 'text'):
                            raw_output = output_obj[0].text
                        else:
                            raw_output = str(output_obj)

                        clean_output = clean_dbt_output(raw_output)

                        # If it's a 'show' or 'metricflow_query' tool, display a preview
                        if tool_name in ['show', 'metricflow_query', 'metricflow_list_metrics', 'metricflow_list_dimensions', 'metricflow_list_semantic_models']:
                            st.code(clean_output)

                        tool_msg = {
                            'role': 'tool',
                            'content': clean_output,
                            'name': tool_name
                        }
                        messages.append(tool_msg)
                        st.session_state.messages.append(tool_msg)
                        status.update(label=f"Used dbt-mcp integration", state="complete")
                    except Exception as e:
                        error_msg = f"Error executing tool: {str(e)}"
                        st.error(error_msg)
                        tool_msg = {
                            'role': 'tool',
                            'content': error_msg,
                            'name': tool_name
                        }
                        messages.append(tool_msg)
                        st.session_state.messages.append(tool_msg)
                        status.update(label=f"Failed dbt-mcp integration", state="error")
        else:
            st.warning("Max iterations reached.")

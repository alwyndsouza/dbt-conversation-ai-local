# Agent Instructions — dbt Local Agent

This file provides instructions and context for AI agents working on this repository.

## Project Context
This is a local AI agent for dbt projects. It uses DuckDB as the database, dbt-mcp for tool calling, Ollama for local LLM inference, and Streamlit for the chat UI. The dbt project includes a layered architecture (Staging → Intermediate → Marts) with a MetricFlow-based Semantic Layer.

## Key Components
- **dbt Project**: Standard dbt structure. Models are in `models/`.
- **Semantic Layer**: Metrics and semantic models in `models/semantic_layer/`.
- **Streamlit App** (`streamlit_app.py`): Chat interface where Ollama translates natural language into dbt-mcp tool calls.
- **dbt-mcp**: Exposes 8 dbt CLI tools + 4 custom MetricFlow CLI tools.

## Available Tools
| Category | Tools |
|---|---|
| dbt CLI (8) | `build`, `compile`, `docs`, `list`, `parse`, `run`, `test`, `show` |
| MetricFlow (4) | `metricflow_list_metrics`, `metricflow_list_dimensions`, `metricflow_list_semantic_models`, `metricflow_query` |

## Development Workflows

### Setup
```bash
pip install -r requirements.txt
dbt seed && dbt run && dbt parse
```

### Run the App
```bash
streamlit run streamlit_app.py
```

### Testing
- Run dbt tests: `dbt test`
- Verify MCP tools: `python scripts/check_mcp_tools.py`

## Coding Standards
- **dbt**: Use explicit references `{{ ref('...') }}`. Follow the layered architecture (staging → intermediate → marts).
- **Python**: Set environment variables before importing `dbt_mcp`. Use `asyncio.run()` for MCP tool interactions.
- **Streamlit**: Use `st.status` for tool calls to provide visual feedback.

## Configuration
All settings are in `.env`:
```env
DISABLE_SEMANTIC_LAYER=true   # Local MetricFlow CLI is used instead
DISABLE_DISCOVERY=true        # No dbt Cloud
DISABLE_REMOTE=true           # No dbt Cloud
DBT_PROJECT_DIR=.
DBT_PROFILES_DIR=.
```

## Common Issues & Troubleshooting
- **MetricFlow Manifest**: If `mf` commands fail with "Unable to load the semantic manifest", run `dbt parse`.
- **Ollama**: Ensure the server is running (`ollama serve`) and a model is pulled (`ollama pull llama3.2`).
- **dbt-mcp Config**: Ensure the three `DISABLE_*` env vars are set to `true` for local-only operation.
- **Tool registration**: If MetricFlow tools are missing, verify `mf --version` works in the active virtualenv.

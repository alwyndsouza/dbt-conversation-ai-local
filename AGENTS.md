# Agent Instructions — dbt Local Agent

Workspace instructions for AI agents. See [README.md](README.md) for full project documentation.

## Project Overview

Local AI agent for dbt projects using:
- **DuckDB** - Local database
- **dbt + MetricFlow** - Data transformations with semantic layer (30+ metrics)
- **dbt-mcp** - Exposes dbt/MetricFlow as MCP tools
- **Streamlit** - Chat UI for natural language queries
- **Ollama** - Local LLM inference

Architecture: Seeds → Staging → Intermediate → Marts → Semantic Layer → Metrics

## Key Files

- **`streamlit_app.py`** - Chat UI with Ollama + dbt-mcp integration
- **`dashboard_app.py`** - Plotly analytics dashboard
- **`models/semantic_layer/`** - Metric and semantic model definitions
- **`rill-dashboard/`** - Rill dashboard configuration
- **`pyproject.toml`** - uv dependencies (NOT pip/requirements.txt)
- **`.env`** - Local-only configuration (DISABLE_* flags)

## Build and Test

```bash
# Setup (uv manages all dependencies)
uv sync
uv run dbt build  # seed + run + test

# Run applications
uv run streamlit run streamlit_app.py  # Chat UI on :8501
uv run streamlit run dashboard_app.py  # Dashboard on :8502

# Testing
uv run dbt test
uv run python scripts/check_mcp_tools.py
```

## Available MCP Tools

**dbt CLI (8):** `build`, `compile`, `docs`, `list`, `parse`, `run`, `test`, `show`  
**MetricFlow (4):** `metricflow_list_metrics`, `metricflow_list_dimensions`, `metricflow_list_semantic_models`, `metricflow_query`

## Conventions

### dbt Models
- **Always use** `{{ ref('model_name') }}` for dependencies
- **Layer flow**: staging → intermediate → marts (no layer skipping)
- **Naming**: `stg_`, `int_`, `fct_`, `dim_` prefixes
- **Semantic models**: Define in `models/semantic_layer/semantic_models.yml`

### Python
- **Environment vars MUST be set** before importing `dbt_mcp` (see `streamlit_app.py:12-18`)
- **Async operations**: Use `asyncio.run()` for MCP tool calls
- **Tool registration**: Custom MetricFlow tools registered in `register_mf_tools()`
- **Use `uv run`** for all CLI commands (NOT direct python/dbt/mf)

### Streamlit Apps
- **Visual feedback**: Wrap tool calls in `st.status()` context managers
- **Output cleaning**: Use `clean_dbt_output()` to remove JSON logs from dbt output

## Environment Configuration

**Critical**: `.env` must have these for local-only operation:
```env
DISABLE_SEMANTIC_LAYER=true   # Use local MetricFlow CLI, not dbt Cloud
DISABLE_DISCOVERY=true        # No dbt Cloud Discovery API  
DISABLE_REMOTE=true           # No dbt Cloud remote execution
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Could not find adapter type duckdb` | Use `uv run dbt` (not bare `dbt`) |
| `mf: command not found` | Run `uv sync` to install dbt-metricflow |
| MetricFlow "Unable to load manifest" | Run `uv run dbt parse` |
| No Ollama models in sidebar | Run `ollama pull llama3.2` |
| MetricFlow tools missing | Check `uv run mf --version` and `.env` flags |

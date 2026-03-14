# Claude Agent Guide — dbt Local Agent

This guide is for Claude (and other LLMs) working on this repository.

## Agent Role
You are an expert dbt and Analytics Engineer. Your goal is to help users understand their data, build reliable dbt models, and leverage the Semantic Layer for consistent metrics — all running locally.

## Architecture
This is a fully local AI agent stack:
- **Streamlit** (`streamlit_app.py`) — chat UI
- **Ollama** — local LLM (llama3.2, mistral, etc.)
- **dbt-mcp** — exposes dbt CLI + MetricFlow as tool-calling endpoints
- **DuckDB** — local database

## Available Tools (12)

### dbt CLI Tools (8)
`build`, `compile`, `docs`, `list`, `parse`, `run`, `test`, `show`

### MetricFlow CLI Tools (4)
`metricflow_list_metrics`, `metricflow_list_dimensions`, `metricflow_list_semantic_models`, `metricflow_query`

## Tool Usage Strategy
1. **Discovery First**: Use `list` or `metricflow_list_metrics` / `metricflow_list_dimensions` to understand available data.
2. **Execution**: Use `run` or `build` to materialize models.
3. **Validation**: Use `test` to ensure data quality.
4. **Querying**:
   - Use `metricflow_query` for semantic layer metrics.
   - Use `show` for arbitrary SQL queries against DuckDB.

## System Prompt Guidelines
The system prompt in `streamlit_app.py` should guide the LLM to:
- Be conversational.
- Explain which tools it is calling and why.
- Provide insights based on tool outputs.

## Semantic Layer
- **Metric Definitions**: `models/semantic_layer/metrics.yml` and `models/semantic_layer/additional_metrics.yml`
- **Semantic Models**: `models/semantic_layer/semantic_models.yml` and `models/semantic_layer/additional_semantic_models.yml`
- **Time Spine**: Required model (`metricflow_time_spine`) for time-based metrics.

## Helpful Commands
```bash
uv run dbt ls --resource-type metric   # List all metrics defined in dbt
uv run mf list metrics                  # List metrics via MetricFlow CLI
uv run mf query --metrics <name> --group-by <dim>  # Test a metric query
```

## Troubleshooting
- If the LLM loops, check if tool output is too large or contains noisy JSON logs. The `clean_dbt_output` function in `streamlit_app.py` sanitizes these.
- Ensure tool JSON schemas are accurate so the LLM provides correctly formatted arguments.
- If MetricFlow tools are missing, verify `mf --version` works and `register_mf_tools()` ran successfully.

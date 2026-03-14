# dbt Local Agent

A local AI agent for your dbt project — query your semantic layer, run models, and explore metrics using natural language. Powered by **dbt-mcp**, **Ollama** (local LLM), and **Streamlit**. No cloud services or API keys required.

> **100% local and private** — your data and queries never leave your machine.

---

## 🎯 What This Does

This project wires together three things:

1. **dbt + MetricFlow** — a sample dbt project with DuckDB, semantic models, and 30+ metrics.
2. **dbt-mcp** — exposes dbt CLI and MetricFlow as tool-calling endpoints via the Model Context Protocol.
3. **Streamlit + Ollama** — a chat UI where a local LLM calls those tools to answer your questions.

You ask a question in plain English, the LLM picks the right dbt-mcp tool, executes it, and returns the result.

> Looking for the **dbt Cloud** version? See [dbt-cloud-agent](https://github.com/alwyndsouza/dbt-cloud-agent).

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9–3.12**
- **Ollama** — [download here](https://ollama.ai)

### Setup

```bash
# Clone the repository
git clone https://github.com/alwyndsouza/dbt-local-agent.git
cd dbt-local-agent

# Install dependencies using uv
uv sync

# Verify installation
uv run dbt --version  # Should show duckdb plugin

# Pull a local LLM
ollama pull llama3.2

# Build the dbt project
uv run dbt build
```

### Launch

```bash
uv run streamlit run streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501).

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Streamlit Chat UI                  │
│               (streamlit_app.py)                     │
└──────────────────────┬──────────────────────────────┘
                       │ natural language
                       ▼
┌─────────────────────────────────────────────────────┐
│              Ollama (Local LLM)                      │
│           llama3.2 / mistral / etc.                  │
└──────────────────────┬──────────────────────────────┘
                       │ tool calls
                       ▼
┌─────────────────────────────────────────────────────┐
│                  dbt-mcp Server                      │
│                                                      │
│  dbt CLI Tools          MetricFlow CLI Tools         │
│  ─────────────          ────────────────────         │
│  build, run, test       metricflow_list_metrics      │
│  compile, parse         metricflow_list_dimensions   │
│  list, show, docs       metricflow_list_semantic_models │
│                         metricflow_query             │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              DuckDB (Local Database)                 │
│                                                      │
│  Seeds → Staging → Intermediate → Marts → Metrics    │
└─────────────────────────────────────────────────────┘
```

### Available Tools (12)

| Category | Tools |
|---|---|
| **dbt CLI** (8) | `build`, `compile`, `docs`, `list`, `parse`, `run`, `test`, `show` |
| **MetricFlow** (4) | `metricflow_list_metrics`, `metricflow_list_dimensions`, `metricflow_list_semantic_models`, `metricflow_query` |

---

## 📊 Semantic Layer

The project includes **6 semantic models** and **30+ metrics** built on a sample orders dataset.

### Semantic Models
| Model | Description |
|---|---|
| **orders** | Order-level transactions and revenue |
| **customers** | Customer lifetime value and segmentation |
| **daily_revenue** | Time-series revenue analysis |
| **geographic_revenue** | Location-based performance |
| **order_status_analysis** | Operational and fulfillment metrics |

### Example MetricFlow Queries

```bash
# List all metrics
mf list metrics

# Revenue by month
mf query --metrics total_revenue --group-by order_date__month

# Revenue and customer count by state
mf query --metrics total_revenue,customer_count --group-by state
```

---

## 💬 Example Prompts

Try these in the chat UI:

- *"Show me all the metrics that are defined"*
- *"What are the dimensions for total_revenue?"*
- *"Show total revenue by state"*
- *"List all staging models"*
- *"Run the dbt project"*

---

## 🛠️ Project Structure

```
dbt-local-agent/
├── streamlit_app.py              # Chat UI + dbt-mcp tool integration
├── dbt_project.yml               # dbt project configuration
├── profiles.yml                  # DuckDB connection profile
├── models/
│   ├── staging/                  # Light transformations (views)
│   ├── intermediate/             # Business logic aggregations (views)
│   ├── marts/                    # Analytics-ready tables
│   └── semantic_layer/           # Metric and semantic model definitions
├── seeds/                        # Sample CSV data (raw_customers, raw_orders)
├── macros/                       # Reusable SQL macros
├── tests/                        # Data quality tests
├── analyses/                     # Ad-hoc analytical queries
├── scripts/                      # Setup and verification scripts
├── .env                          # Environment configuration
└── requirements.txt              # Python dependencies
```

---

## ⚙️ Configuration

All settings are in `.env`:

```env
DISABLE_SEMANTIC_LAYER=true   # true = use local MetricFlow CLI tools
DISABLE_DISCOVERY=true        # true = no dbt Cloud Discovery API
DISABLE_REMOTE=true           # true = no dbt Cloud remote execution
DBT_PROJECT_DIR=.
DBT_PROFILES_DIR=.
```

These are the correct settings for fully local operation.

---

## ⚠️ Troubleshooting

| Problem | Fix |
|---|---|
| `Could not find adapter type duckdb!` | Use `uv run dbt` to ensure the correct environment is used |
| `No module named 'dbt.adapters.duckdb'` | Use `uv run` to execute commands |
| `mf: command not found` | Ensure dependencies are synced: `uv sync` |
| No metrics found | Run `dbt parse` to generate the semantic manifest |
| Ollama connection error | Ensure Ollama is running: `ollama serve` |
| No models in sidebar | Pull a model: `ollama pull llama3.2` |

---

## 📚 Resources

- [dbt Documentation](https://docs.getdbt.com/)
- [MetricFlow Commands](https://docs.getdbt.com/docs/build/metricflow-commands)
- [dbt-mcp](https://github.com/dbt-labs/dbt-mcp)
- [Ollama](https://ollama.ai)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

## 📄 License

MIT

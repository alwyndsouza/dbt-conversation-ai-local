# Rill Project

This project is a **code-first Rill** analytics project using a local, managed **DuckDB** OLAP connector (read/write). Source data lives as **Parquet files in `/data`** and is loaded/transformed into DuckDB via **Rill models**.

## Quick start

```bash
rill start
```

Open the UI at:

- http://localhost:9009

## Data & models

Parquet sources (in `/data`):
- `fct_orders.parquet`
- `fct_customers.parquet`
- `fct_daily_orders.parquet`
- `fct_revenue_by_state.parquet`

Models (in `/models`) load and transform these sources:
- `orders.sql`
- `customers.sql`
- `orders_enriched.sql`
- `daily_orders.sql`
- `state_revenue.sql`

## Metrics & dashboards

Metrics view:
- `orders_analytics_metrics` (defined in `metrics/orders_analytics_metrics.yaml`)

Available dashboards:
- **Explore: `orders_analytics_explore`** (`dashboards/orders_analytics_explore.yaml`) — interactive slice-and-dice exploration of the orders analytics metrics.
- **Canvas: `orders_analytics_canvas`** (`dashboards/orders_analytics_canvas.yaml`) — curated overview dashboard built as a code-first canvas.
- **Canvas: `orders_exec_pack_canvas`** (`dashboards/orders_exec_pack_canvas.yaml`) — executive-style pack / summary view built as a code-first canvas.

> Note: Canvases in this project are defined in YAML (code-first). You can still iterate on dashboards in the UI, but the canonical definitions live in the project files.

## Project structure

```text
.
├── dashboards
│   ├── orders_analytics_canvas.yaml
│   ├── orders_analytics_explore.yaml
│   └── orders_exec_pack_canvas.yaml
├── data
│   ├── fct_customers.parquet
│   ├── fct_daily_orders.parquet
│   ├── fct_orders.parquet
│   └── fct_revenue_by_state.parquet
├── metrics
│   └── orders_analytics_metrics.yaml
├── models
│   ├── customers.sql
│   ├── daily_orders.sql
│   ├── orders.sql
│   ├── orders_enriched.sql
│   └── state_revenue.sql
└── rill.yaml
```

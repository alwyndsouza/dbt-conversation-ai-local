# Orders Analytics Dashboard

A Rill dashboard project that mirrors the Streamlit `dashboard_app.py` for e-commerce orders analytics.

## Overview

This dashboard provides comprehensive e-commerce analytics including:
- **KPI Metrics**: Total Revenue, Orders, Customers, Average Order Value
- **Revenue Trends**: Line charts showing revenue over time
- **Order Status Breakdown**: Completed, Pending, Cancelled orders
- **Geographic Analysis**: Revenue by state
- **Customer Segmentation**: High/Medium/Low value customers
- **Daily Order Details**: Trend charts for each order status

## Data Sources

The dashboard connects to the main DuckDB database (`dbt-conversation-ai-local.duckdb`) and uses these dbt models:
- `fct_daily_orders` - Daily aggregated order metrics
- `fct_orders` - Individual order records
- `fct_customers` - Customer profiles with segments
- `fct_revenue_by_state` - State-level revenue aggregation

## Quick Start

```bash
# Start Rill dashboard
cd rill-dashboard
rill start
```

Then open http://localhost:9009 in your browser.

## Available Dashboard

Once Rill is running, navigate to:
- **Explore** → `orders_analytics_explore`

This will give you access to:
- Dimensions: order_date, state, customer_segment, customer_id, customer_name, city, order_year, order_month
- Measures: total_revenue, total_orders, completed_orders, pending_orders, cancelled_orders, unique_customers, total_customers, avg_order_value, completion_rate

## MetricsView

The `orders_analytics_metrics` MetricsView provides:
- Time dimension: `order_date`
- Categorical dimensions: state, customer_segment, customer_id, customer_name, email, city, order_year, order_month
- Measures: All KPI metrics with proper formatting (currency, percentage, number)

## Files Structure

```
rill-dashboard/
├── rill.yaml                    # Project configuration
├── connectors/
│   └── duckdb.yaml             # DuckDB connector
├── models/
│   ├── daily_orders.sql        # Daily orders model
│   ├── orders.sql              # Orders model
│   ├── customers.sql           # Customers model
│   └── state_revenue.sql       # State revenue model
├── metrics/
│   └── orders_analytics_metrics.yaml  # MetricsView definition
└── dashboards/
    └── orders_analytics_explore.yaml  # Explore/dashboard definition
```

## Matching the Streamlit Dashboard

The Streamlit dashboard (`dashboard_app.py`) visualizations that can be replicated in Rill:

| Streamlit Component | Rill Visualization |
|---------------------|-------------------|
| KPI Cards (4 metrics) | Leaderboard with 4 measures |
| Revenue Trend Line Chart | Time series chart |
| Order Status Donut | Pie chart |
| Revenue by State Bar | Horizontal bar chart |
| Customer Segments Pie | Pie chart |
| Daily Order Charts (3) | 3 Time series charts |
| Data Tables | Tables |
| Top Customers | Leaderboard |

## Usage

1. **Start Rill**: `rill start`
2. **Open browser**: http://localhost:9009
3. **Navigate to Explore**: Click "Explore" in the left sidebar
4. **Select Metrics View**: Choose `orders_analytics_explore`
5. **Build visualizations**: Use the dimension/measure selectors to create charts
6. **Save as Dashboard**: Use Rill's UI to save your custom dashboard

## Note

The dashboard is pre-configured with the MetricsView and Explore definitions. The actual dashboard widgets should be built interactively in the Rill UI for the best experience, as Rill's interactive builder provides a better experience than static YAML configurations for complex layouts.

# Rill Dashboard - Orders Analytics

A Rill-based analytics dashboard for your e-commerce orders data.

## Project Structure

```
rill-dashboard/
├── rill.yml                 # Project configuration
├── sources/                # Data source definitions
│   ├── orders.yml
│   ├── daily_orders.yml
│   ├── customers.yml
│   └── state_revenue.yml
├── models/                 # SQL transformations
│   └── orders.sql
├── dashboards/             # Dashboard definitions
│   └── orders_analytics.yml
└── *.parquet              # Data files
```

## Getting Started

1. **Install Rill:**
   ```bash
   curl -fsSL https://rill.sh | sh
   ```

2. **Navigate to the project:**
   ```bash
   cd rill-dashboard
   ```

3. **Start Rill:**
   ```bash
   rill start
   ```

4. **Open the dashboard:**
   - Rill will open http://localhost:9009 in your browser
   - Navigate to the "Orders Analytics" dashboard

## Dashboard Features

### Overview Page
- **KPI Cards:** Total Revenue, Orders, Avg Order Value, Customers
- **Revenue Trend:** Area chart showing revenue over time
- **Order Status:** Pie chart (Completed/Pending/Cancelled)
- **Revenue by State:** Bar chart

### Customer Analysis Page
- **Customer Segments:** Pie chart breakdown
- **Revenue by Segment:** Bar chart
- **Top Customers:** Table with revenue and order details

## Data Model

| Source | Description | Rows |
|--------|-------------|------|
| orders | Order transactions | 15 |
| daily_orders | Daily aggregations | 15 |
| customers | Customer profiles | 9 |
| state_revenue | Geographic data | 15 |

## Metrics

| Metric | Formula |
|--------|---------|
| Total Revenue | sum(order_total) |
| Total Orders | count(*) |
| Avg Order Value | avg(order_total) |
| Completed Orders | countIf(status='completed') |
| Total Customers | count(distinct customer_id) |

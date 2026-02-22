-- Geographic Analysis
-- Analyzes customer and order distribution by state

with customers as (
    select * from {{ ref('fct_customers') }}
),

state_metrics as (
    select
        state,
        count(*) as customer_count,
        sum(total_revenue) as total_revenue,
        avg(total_revenue) as avg_revenue_per_customer,
        sum(total_orders) as total_orders,
        avg(total_orders) as avg_orders_per_customer
    from customers
    group by state
)

select
    state,
    customer_count,
    round(total_revenue, 2) as total_revenue,
    round(avg_revenue_per_customer, 2) as avg_revenue_per_customer,
    total_orders,
    round(avg_orders_per_customer, 2) as avg_orders_per_customer,
    round(total_revenue / nullif(sum(total_revenue) over (), 0) * 100, 2) as revenue_share_pct
from state_metrics
order by total_revenue desc

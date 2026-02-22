-- Customer Lifetime Value Analysis
-- This analysis calculates customer segments based on their lifetime value

with customer_metrics as (
    select * from {{ ref('fct_customers') }}
),

customer_ltv as (
    select
        customer_segment,
        count(*) as customer_count,
        sum(total_revenue) as segment_revenue,
        avg(total_revenue) as avg_revenue_per_customer,
        avg(total_orders) as avg_orders_per_customer,
        avg(avg_order_value) as avg_order_value
    from customer_metrics
    group by customer_segment
)

select
    customer_segment,
    customer_count,
    segment_revenue,
    round(avg_revenue_per_customer, 2) as avg_revenue_per_customer,
    round(avg_orders_per_customer, 2) as avg_orders_per_customer,
    round(avg_order_value, 2) as avg_order_value,
    round(segment_revenue / nullif(sum(segment_revenue) over (), 0) * 100, 2) as revenue_percentage
from customer_ltv
order by segment_revenue desc

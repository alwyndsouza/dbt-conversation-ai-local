-- Order Trends Analysis
-- Analyzes order patterns by time period

with orders as (
    select * from {{ ref('fct_orders') }}
),

monthly_trends as (
    select
        order_year,
        order_month,
        count(*) as total_orders,
        sum(case when order_status = 'completed' then 1 else 0 end) as completed_orders,
        sum(case when order_status = 'pending' then 1 else 0 end) as pending_orders,
        sum(case when order_status = 'cancelled' then 1 else 0 end) as cancelled_orders,
        sum(case when order_status = 'completed' then order_total else 0 end) as total_revenue,
        avg(case when order_status = 'completed' then order_total else null end) as avg_order_value
    from orders
    group by order_year, order_month
)

select
    order_year,
    order_month,
    total_orders,
    completed_orders,
    pending_orders,
    cancelled_orders,
    round(total_revenue, 2) as total_revenue,
    round(avg_order_value, 2) as avg_order_value,
    round(completed_orders::float / nullif(total_orders, 0) * 100, 2) as completion_rate
from monthly_trends
order by order_year, order_month

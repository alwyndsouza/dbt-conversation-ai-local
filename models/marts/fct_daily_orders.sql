with daily_orders as (
    select * from {{ ref('fct_orders') }}
),

daily_aggregates as (
    select
        order_date,
        count(*) as order_count,
        count(distinct customer_id) as unique_customers,
        sum(case when order_status = 'completed' then order_total else 0 end) as revenue,
        sum(case when order_status = 'completed' then 1 else 0 end) as completed_orders,
        sum(case when order_status = 'pending' then 1 else 0 end) as pending_orders,
        sum(case when order_status = 'cancelled' then 1 else 0 end) as cancelled_orders,
        avg(case when order_status = 'completed' then order_total else null end) as avg_order_value
    from daily_orders
    group by order_date
)

select * from daily_aggregates

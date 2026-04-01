with daily_orders as (
    select
        order_date,
        order_total,
        order_status,
        customer_id
    from {{ ref('fct_orders') }}
),

daily_aggregates as (
    select
        order_date,
        count(*) as order_count,
        count(distinct customer_id) as unique_customers,
        {{ order_status_counts('order_total', 'order_status') }},
        avg(case when order_status = 'completed' then order_total else null end) as avg_order_value
    from daily_orders
    group by order_date
)

select * from daily_aggregates

with orders as (
    select
        customer_id,
        order_total,
        order_status,
        order_date
    from {{ ref('stg_orders') }}
),

customer_orders as (
    select
        customer_id,
        count(*) as total_orders,
        {{ order_status_counts('order_total', 'order_status') }},
        avg(case when order_status = 'completed' then order_total else null end) as avg_order_value,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date
    from orders
    group by customer_id
)

select * from customer_orders

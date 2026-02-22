with orders as (
    select * from {{ ref('stg_orders') }}
),

customer_orders as (
    select
        customer_id,
        count(*) as total_orders,
        sum(case when order_status = 'completed' then 1 else 0 end) as completed_orders,
        sum(case when order_status = 'pending' then 1 else 0 end) as pending_orders,
        sum(case when order_status = 'cancelled' then 1 else 0 end) as cancelled_orders,
        sum(case when order_status = 'completed' then order_total else 0 end) as total_revenue,
        avg(case when order_status = 'completed' then order_total else null end) as avg_order_value,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date
    from orders
    group by customer_id
)

select * from customer_orders

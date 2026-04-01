with orders as (
    select
        order_id,
        customer_id,
        order_date,
        order_total,
        order_status,
        order_year,
        order_month,
        order_day,
        order_day_of_week
    from {{ ref('stg_orders') }}
),

customers as (
    select
        customer_id,
        customer_name,
        email,
        city,
        state
    from {{ ref('stg_customers') }}
),

final as (
    select
        o.order_id,
        o.customer_id,
        c.customer_name,
        c.email,
        c.city,
        c.state,
        o.order_date,
        o.order_total,
        o.order_status,
        o.order_year,
        o.order_month,
        o.order_day,
        o.order_day_of_week
    from orders o
    left join customers c on o.customer_id = c.customer_id
)

select * from final

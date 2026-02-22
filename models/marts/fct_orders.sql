with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
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
        extract(year from o.order_date) as order_year,
        extract(month from o.order_date) as order_month,
        extract(day from o.order_date) as order_day,
        extract(dayofweek from o.order_date) as order_day_of_week
    from orders o
    left join customers c on o.customer_id = c.customer_id
)

select * from final

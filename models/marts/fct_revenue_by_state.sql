with orders as (
    select * from {{ ref('fct_orders') }}
),

state_aggregates as (
    select
        state,
        order_date,
        count(*) as order_count,
        count(distinct customer_id) as unique_customers,
        sum(case when order_status = 'completed' then order_total else 0 end) as revenue,
        avg(case when order_status = 'completed' then order_total else null end) as avg_order_value
    from orders
    group by state, order_date
)

select * from state_aggregates

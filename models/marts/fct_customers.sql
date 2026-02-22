with customers as (
    select * from {{ ref('stg_customers') }}
),

customer_summary as (
    select * from {{ ref('int_customer_order_summary') }}
),

final as (
    select
        c.customer_id,
        c.customer_name,
        c.email,
        c.city,
        c.state,
        c.joined_date,
        coalesce(cs.total_orders, 0) as total_orders,
        coalesce(cs.completed_orders, 0) as completed_orders,
        coalesce(cs.pending_orders, 0) as pending_orders,
        coalesce(cs.cancelled_orders, 0) as cancelled_orders,
        coalesce(cs.total_revenue, 0) as total_revenue,
        cs.avg_order_value,
        cs.first_order_date,
        cs.last_order_date,
        case 
            when cs.total_revenue >= 500 then 'High Value'
            when cs.total_revenue >= 200 then 'Medium Value'
            when cs.total_revenue > 0 then 'Low Value'
            else 'No Purchases'
        end as customer_segment
    from customers c
    left join customer_summary cs on c.customer_id = cs.customer_id
)

select * from final

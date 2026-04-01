-- Customers Model
SELECT 
    customer_id,
    customer_name,
    email,
    city,
    state,
    CAST(joined_date AS DATE) as joined_date,
    total_orders,
    CAST(completed_orders AS INTEGER) as completed_orders,
    CAST(pending_orders AS INTEGER) as pending_orders,
    CAST(cancelled_orders AS INTEGER) as cancelled_orders,
    total_revenue,
    avg_order_value,
    CAST(first_order_date AS DATE) as first_order_date,
    CAST(last_order_date AS DATE) as last_order_date,
    customer_segment
FROM 'fct_customers'
ORDER BY customer_id

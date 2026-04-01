-- Daily Orders Model
SELECT 
    CAST(order_date AS DATE) as order_date,
    order_count,
    unique_customers,
    CAST(completed_orders AS INTEGER) as completed_orders,
    CAST(pending_orders AS INTEGER) as pending_orders,
    CAST(cancelled_orders AS INTEGER) as cancelled_orders,
    total_revenue,
    avg_order_value
FROM 'fct_daily_orders'
ORDER BY order_date

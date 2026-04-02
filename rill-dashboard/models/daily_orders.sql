-- Daily Orders Model
SELECT 
    CAST(order_date AS DATE) as order_date,
    order_count,
    unique_customers,
    completed_orders,
    pending_orders,
    cancelled_orders,
    total_revenue,
    avg_order_value
FROM fct_daily_orders
ORDER BY order_date

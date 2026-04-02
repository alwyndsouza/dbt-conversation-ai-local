-- State Revenue Model
SELECT 
    state,
    CAST(order_date AS DATE) as order_date,
    order_count,
    unique_customers,
    CAST(completed_orders AS INTEGER) as completed_orders,
    CAST(pending_orders AS INTEGER) as pending_orders,
    CAST(cancelled_orders AS INTEGER) as cancelled_orders,
    total_revenue,
    avg_order_value
FROM 'data/fct_revenue_by_state.parquet'
ORDER BY state, order_date

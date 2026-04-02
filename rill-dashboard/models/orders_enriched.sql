-- Orders Enriched Model
-- Joins order details with customer dimensions for the dashboard
SELECT
    o.order_id,
    o.customer_id,
    o.customer_name,
    o.email,
    o.city,
    o.state,
    CAST(o.order_date AS DATE) as order_date,
    o.order_total,
    o.order_status,
    o.order_year,
    o.order_month,
    c.customer_segment,
    CASE WHEN o.order_status = 'completed' THEN 1 ELSE 0 END as completed_order,
    CASE WHEN o.order_status = 'pending' THEN 1 ELSE 0 END as pending_order,
    CASE WHEN o.order_status = 'cancelled' THEN 1 ELSE 0 END as cancelled_order,
    CASE WHEN o.order_status = 'completed' THEN o.order_total ELSE 0 END as revenue
FROM fct_orders o
LEFT JOIN fct_customers c ON o.customer_id = c.customer_id
ORDER BY o.order_date DESC

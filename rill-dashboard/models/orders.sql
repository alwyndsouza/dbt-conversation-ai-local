-- Orders model combining order details with customer info
SELECT 
    o.order_id,
    o.customer_id,
    o.customer_name,
    o.email,
    o.city,
    o.state,
    o.order_date,
    o.order_total,
    o.order_status,
    o.order_year,
    o.order_month,
    o.order_day,
    c.customer_segment,
    c.total_revenue as customer_lifetime_value,
    c.total_orders as customer_total_orders
FROM 'orders.parquet' o
LEFT JOIN 'customers.parquet' c ON o.customer_id = c.customer_id

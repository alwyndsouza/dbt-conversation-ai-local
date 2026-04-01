-- Orders Model
SELECT 
    order_id,
    customer_id,
    customer_name,
    email,
    city,
    state,
    CAST(order_date AS DATE) as order_date,
    order_total,
    order_status,
    order_year,
    order_month,
    order_day,
    order_day_of_week
FROM 'fct_orders'
ORDER BY order_date DESC

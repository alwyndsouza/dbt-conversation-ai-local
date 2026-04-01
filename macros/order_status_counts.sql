{#
    Calculate order status counts from an order_total column.
    
    Usage:
        {{ order_status_counts('order_total', 'order_status') }}
    
    Returns:
        - completed_orders, pending_orders, cancelled_orders
#}
{% macro order_status_counts(order_total_col='order_total', status_col='order_status') %}
    sum(case when {{ status_col }} = 'completed' then 1 else 0 end) as completed_orders,
    sum(case when {{ status_col }} = 'pending' then 1 else 0 end) as pending_orders,
    sum(case when {{ status_col }} = 'cancelled' then 1 else 0 end) as cancelled_orders,
    sum(case when {{ status_col }} = 'completed' then {{ order_total_col }} else 0 end) as total_revenue
{% endmacro %}

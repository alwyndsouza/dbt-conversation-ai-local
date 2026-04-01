{#
    Calculate order count by status from a status column.
    Use this when you don't need revenue calculations.
    
    Usage:
        {{ order_count_by_status('order_status') }}
    
    Returns:
        - completed_count, pending_count, cancelled_count
#}
{% macro order_count_by_status(status_col='order_status') %}
    sum(case when {{ status_col }} = 'completed' then 1 else 0 end) as completed_count,
    sum(case when {{ status_col }} = 'pending' then 1 else 0 end) as pending_count,
    sum(case when {{ status_col }} = 'cancelled' then 1 else 0 end) as cancelled_count
{% endmacro %}

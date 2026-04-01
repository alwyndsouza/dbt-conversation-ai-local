{#
    Assign customer segment based on total revenue thresholds.
    
    Usage:
        {{ customer_segment('total_revenue') }}
    
    Requires vars:
        - customer_segment_high: threshold for High Value (default: 500)
        - customer_segment_medium: threshold for Medium Value (default: 200)
    
    Returns:
        - 'High Value', 'Medium Value', 'Low Value', or 'No Purchases'
#}
{% macro customer_segment(revenue_col='total_revenue') %}
    case 
        when {{ revenue_col }} >= {{ var('customer_segment_high', 500) }} then 'High Value'
        when {{ revenue_col }} >= {{ var('customer_segment_medium', 200) }} then 'Medium Value'
        when {{ revenue_col }} > 0 then 'Low Value'
        else 'No Purchases'
    end
{% endmacro %}

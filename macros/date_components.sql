{#
    Extract date components from a date column.
    
    Usage:
        {{ date_components('order_date', 'order_') }}
    
    Returns:
        - {prefix}year, {prefix}month, {prefix}day, {prefix}day_of_week
#}
{% macro date_components(date_col, prefix='') %}
    extract(year from {{ date_col }}) as {{ prefix }}year,
    extract(month from {{ date_col }}) as {{ prefix }}month,
    extract(day from {{ date_col }}) as {{ prefix }}day,
    extract(dayofweek from {{ date_col }}) as {{ prefix }}day_of_week
{% endmacro %}

{{ config(materialized='table') }}

with date_spine as (
    {{ dbt.date_spine(
        datepart="day",
        start_date="cast('2022-01-01' as date)",
        end_date="cast('2025-12-31' as date)"
    )}}
)

select
    date_day
from date_spine

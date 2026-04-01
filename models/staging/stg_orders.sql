with source as (
    select * from {{ ref('raw_orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        order_date::date as order_date,
        order_total::decimal(10,2) as order_total,
        status as order_status,
        -- Date components using macro
        {{ date_components('order_date', 'order_') }}
    from source
)

select * from renamed

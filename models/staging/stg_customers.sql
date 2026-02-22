with source as (
    select * from {{ ref('raw_customers') }}
),

renamed as (
    select
        customer_id,
        customer_name,
        email,
        city,
        state,
        joined_date::date as joined_date
    from source
)

select * from renamed

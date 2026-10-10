
select
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    province,
    country,
    is_active

from {{ ref('stg_walmart__customers') }}

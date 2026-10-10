
select
    store_id,
    store_name,
    city,
    province,
    country,
    is_active

from {{ ref('stg_walmart__stores') }}

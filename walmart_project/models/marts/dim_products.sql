
select
    product_id,
    product_name,
    category,
    brand,
    price,
    is_active

from {{ ref('stg_walmart__products') }}

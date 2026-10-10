
with order_items as (

    select *
    from {{ ref('stg_walmart__order_items') }}

),

orders as (

    select *
    from {{ ref('stg_walmart__orders') }}

),

products as (

    select *
    from {{ ref('stg_walmart__products') }}

),

enriched as (

    select
        oi.order_item_id,
        oi.order_id,
        o.customer_id,
        o.store_id,

        oi.product_id,
        p.product_name,
        p.category,
        p.brand,

        oi.quantity,
        oi.unit_price,
        oi.line_amount,

        o.order_timestamp,
        o.order_status

    from order_items as oi

    left join orders as o
        on oi.order_id = o.order_id

    left join products as p
        on oi.product_id = p.product_id

)

select *
from enriched

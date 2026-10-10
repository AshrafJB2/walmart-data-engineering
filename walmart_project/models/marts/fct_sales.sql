
with order_items as (

    select *
    from {{ ref('int_order_items_enriched') }}

)

select
    order_item_id,
    order_id,

    customer_id,
    product_id,
    store_id,

    order_timestamp,
    order_status,

    quantity,
    unit_price,
    line_amount

from order_items

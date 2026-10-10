
select
    order_id,
    customer_id,
    store_id,

    order_timestamp,
    order_status,

    source_total_amount,
    calculated_total_amount,

    total_quantity,
    order_item_count

from {{ ref('int_orders_with_totals') }}


with orders as (

    select *
    from {{ ref('stg_walmart__orders') }}

),

order_items as (

    select *
    from {{ ref('stg_walmart__order_items') }}

),

item_totals as (

    select
        order_id,
        sum(line_amount) as calculated_total_amount,
        sum(quantity) as total_quantity,
        count(*) as order_item_count

    from order_items
    group by order_id

),

final as (

    select
        o.order_id,
        o.customer_id,
        o.store_id,
        o.order_timestamp,
        o.order_status,

        o.total_amount as source_total_amount,
        coalesce(i.calculated_total_amount, 0)
            as calculated_total_amount,

        coalesce(i.total_quantity, 0) as total_quantity,
        coalesce(i.order_item_count, 0) as order_item_count

    from orders as o

    left join item_totals as i
        on o.order_id = i.order_id

)

select *
from final

{{ config(
    materialized='incremental',
    unique_key='order_item_id',
) }}

SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    line_amount,
    created_timestamp,
    updated_timestamp,
    is_active,
    current_timestamp() AS dbt_updated_at
FROM {{ source('walmart_source', 'order_items') }}

{% if is_incremental() %}
WHERE updated_timestamp >= coalesce(
    (SELECT max(updated_timestamp) FROM {{ this }}),
    CAST('1900-01-01' AS TIMESTAMP)
)
{% endif %}
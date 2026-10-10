{{ config(
    materialized='incremental',
    unique_key='product_id',
) }}

SELECT
    product_id,
    product_name,
    category,
    brand,
    price,
    created_timestamp,
    updated_timestamp,
    is_active,
    current_timestamp() AS dbt_updated_at
FROM {{ source('walmart_source', 'products') }}

{% if is_incremental() %}
WHERE updated_timestamp >= coalesce(
    (SELECT max(updated_timestamp) FROM {{ this }}),
    CAST('1900-01-01' AS TIMESTAMP)
)
{% endif %}
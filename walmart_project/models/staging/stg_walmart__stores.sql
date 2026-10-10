{{ config(
    materialized='incremental',
    unique_key='store_id',
) }}

SELECT
    store_id,
    store_name,
    city,
    province,
    country,
    created_timestamp,
    updated_timestamp,
    is_active,
    current_timestamp() AS dbt_updated_at
FROM {{ source('walmart_source', 'stores') }}

{% if is_incremental() %}
WHERE updated_timestamp >= coalesce(
    (SELECT max(updated_timestamp) FROM {{ this }}),
    CAST('1900-01-01' AS TIMESTAMP)
)
{% endif %}
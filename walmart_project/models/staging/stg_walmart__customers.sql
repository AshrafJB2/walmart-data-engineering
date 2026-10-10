{{ config(
    materialized='incremental',
    unique_key='customer_id',
) }}

SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    province,
    country,
    created_timestamp,
    updated_timestamp,
    is_active,
    current_timestamp() AS dbt_updated_at
FROM {{ source('walmart_source', 'customers') }}

{% if is_incremental() %}
WHERE updated_timestamp >= coalesce(
    (SELECT max(updated_timestamp) FROM {{ this }}),
    CAST('1900-01-01' AS TIMESTAMP)
)
{% endif %}
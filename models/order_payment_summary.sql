{{
  config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='fail',
    alias='fct_order_payments',
    post_hook="COMMENT ON TABLE {{ this }} IS 'Incremental order payment summary — built by dbt'"
  )
}}

-- Incremental model: summarizes order payments.
-- On incremental runs, only processes orders placed since the last run.

select
    order_id,
    customer_id,
    order_date,
    status,
    total_payment_amount,
    payment_count,
    current_timestamp as loaded_at
from {{ ref('int_order_payments') }}

{% if is_incremental() %}
  where order_date > (select max(order_date) from {{ this }})
{% endif %}

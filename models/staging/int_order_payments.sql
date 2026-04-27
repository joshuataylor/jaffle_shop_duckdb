{{
  config(
    materialized='ephemeral'
  )
}}

-- Ephemeral intermediate model: joins orders with their payment totals.
-- This is injected as a CTE into downstream models, never materialized.

select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    sum(p.amount) as total_payment_amount,
    count(p.payment_id) as payment_count
from {{ ref('stg_orders') }} as o
left join {{ ref('stg_payments') }} as p on o.order_id = p.order_id
{{ dbt_utils.group_by(4) }}

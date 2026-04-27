{{ config(
    severity='warn',
    error_if='>5',
    warn_if='>0',
    store_failures=true,
    tags=['payments', 'data_quality']
) }}

-- Refunds have a negative amount, so the total amount should always be >= 0.
-- Therefore return records where total_amount < 0 to make the test fail.
-- Configured to warn on any failures and only error if more than 5 orders
-- are affected; failures are persisted to the warehouse for triage.
select
    stg_payments.order_id,
    sum(stg_payments.amount) as total_amount
from {{ ref('stg_payments') }} as stg_payments
group by stg_payments.order_id
having sum(stg_payments.amount) < 0

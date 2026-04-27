-- Demonstrates pinning a ref() to a specific model version.
-- Uses v2 of the customers model to access the customer_status column,
-- which doesn't exist in v1. Compiled but not materialised.

select
    customer_status,
    count(*) as customer_count,
    sum(customer_lifetime_value) as total_clv,
    avg(number_of_orders) as avg_orders_per_customer
from {{ ref('customers', v=2) }}
group by customer_status
order by customer_count desc

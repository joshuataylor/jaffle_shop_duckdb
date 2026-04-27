-- Customer cohort analysis: monthly acquisition cohorts and their order counts.
-- This analysis is compiled but not materialized — useful for ad-hoc queries
-- that benefit from Jinja templating and ref().

with customers as (
    select * from {{ ref('customers', v=1) }}
),

orders as (
    select * from {{ ref('orders') }}
),

cohorts as (
    select
        date_trunc('month', c.first_order) as cohort_month,
        date_trunc('month', o.order_date) as order_month,
        count(distinct c.customer_id) as customers,
        count(o.order_id) as orders,
        sum(o.amount) as revenue
    from customers c
    inner join orders o on c.customer_id = o.customer_id
    where c.first_order is not null
    group by 1, 2
)

select
    cohort_month,
    order_month,
    customers,
    orders,
    revenue,
    datediff('month', cohort_month, order_month) as months_since_first_order
from cohorts
order by cohort_month, order_month

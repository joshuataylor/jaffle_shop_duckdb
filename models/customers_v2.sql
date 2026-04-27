{{ config(materialized='table') }}

-- v2 of the customers model. Adds customer_status, derived from
-- the customer's most_recent_order: 'active' if they've ordered in
-- the last 90 days, 'churned' if longer ago, or 'never_ordered'.

with customers as (

    select * from {{ ref('stg_customers') }}

),

orders as (

    select * from {{ ref('stg_orders') }}

),

payments as (

    select * from {{ ref('stg_payments') }}

),

customer_orders as (

    select
        orders.customer_id,
        min(orders.order_date) as first_order,
        max(orders.order_date) as most_recent_order,
        count(orders.order_id) as number_of_orders
    from orders
    group by orders.customer_id

),

customer_payments as (

    select
        orders.customer_id,
        sum(payments.amount) as total_amount
    from payments
    left join orders on orders.order_id = payments.order_id
    group by orders.customer_id

),

final as (

    select
        {{ dbt_utils.generate_surrogate_key(['customers.customer_id']) }} as customer_key,
        customers.customer_id,
        {% if var('include_pii', true) %}
        customers.first_name,
        customers.last_name,
        {% else %}
        cast(null as varchar) as first_name,
        cast(null as varchar) as last_name,
        {% endif %}
        customer_orders.first_order,
        customer_orders.most_recent_order,
        customer_orders.number_of_orders,
        customer_payments.total_amount as customer_lifetime_value,
        case
            when customer_orders.most_recent_order is null
                then 'never_ordered'
            when customer_orders.most_recent_order
                >= date_add(current_date, interval (-90) day)
                then 'active'
            else 'churned'
        end as customer_status

    from customers
    left join customer_orders on customer_orders.customer_id = customers.customer_id
    left join customer_payments on customer_payments.customer_id = customers.customer_id

)

select * from final

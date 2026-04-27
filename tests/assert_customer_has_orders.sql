-- Every customer in the customers table should have at least one order.
select
    c.customer_id
from {{ ref('customers') }} c
left join {{ ref('orders') }} o
    on c.customer_id = o.customer_id
where o.order_id is null
    and c.number_of_orders > 0

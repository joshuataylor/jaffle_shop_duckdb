-- Every customer in the customers table should have at least one order.
select
    customers.customer_id
from {{ ref('customers', v=1) }} as customers
left join {{ ref('orders') }} as orders on orders.customer_id = customers.customer_id
where orders.order_id is null
and customers.number_of_orders > 0

{% docs orders_status %}

Orders can be one of the following statuses:

| status         | description                                                                                                            |
|----------------|------------------------------------------------------------------------------------------------------------------------|
| placed         | The order has been placed but has not yet left the warehouse                                                           |
| shipped        | The order has ben shipped to the customer and is currently in transit                                                  |
| completed      | The order has been received by the customer                                                                            |
| return_pending | The customer has indicated that they would like to return the order, but it has not yet been received at the warehouse |
| returned       | The order has been returned by the customer and received at the warehouse                                              |


{% enddocs %}

{% docs payment_methods %}

Payments can be made using one of the following methods:

| method         | description                                      |
|----------------|--------------------------------------------------|
| credit_card    | Payment via credit card                          |
| coupon         | Payment via a coupon or promotional code         |
| bank_transfer  | Payment via direct bank transfer                 |
| gift_card      | Payment via a gift card                          |

{% enddocs %}

{% docs customer_lifetime_value %}

The total value (in AUD) of all orders placed by a customer over their
lifetime. Calculated as the sum of all payment amounts associated with
the customer's orders, converted from cents to dollars.

{% enddocs %}

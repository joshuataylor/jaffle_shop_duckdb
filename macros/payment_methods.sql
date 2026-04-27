{% macro payment_methods() %}
  {% do return(['credit_card', 'coupon', 'bank_transfer', 'gift_card']) %}
{% endmacro %}

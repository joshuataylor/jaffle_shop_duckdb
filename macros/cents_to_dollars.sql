{% macro cents_to_dollars(column_name, precision=2) %}
    round({{ column_name }} / {{ var('cents_divisor') }}, {{ precision }})
{% endmacro %}

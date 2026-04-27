{% test accepted_range(model, column_name, min_value=0, max_value=none) %}

select *
from {{ model }}
where {{ column_name }} < {{ min_value }}
    {% if max_value is not none %}
    or {{ column_name }} > {{ max_value }}
    {% endif %}

{% endtest %}

{% macro limit_data_in_dev(column_name, dev_days_of_data=none) %}
    {#
      Limits data when running in the 'dev' target. The window defaults
      to the dev_data_days project variable (overridable at runtime via
      --vars '{dev_data_days: 7}'), but can also be passed explicitly.
    #}
    {% set days = dev_days_of_data if dev_days_of_data is not none else var('dev_data_days', 3) %}
    {% if target.name == 'dev' %}
        where {{ column_name }} >= date_add(current_date, interval (-{{ days }}) day)
    {% endif %}
{% endmacro %}

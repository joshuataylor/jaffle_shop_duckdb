{% macro log_table_row_counts() %}
  {#
    A run-operation macro that logs row counts for all mart models.
    Usage: dbt run-operation log_table_row_counts
  #}
  {% set tables = ['customers', 'orders'] %}
  {% for table in tables %}
    {% set query %}
      select count(*) as row_count from {{ ref(table) }}
    {% endset %}
    {% set results = run_query(query) %}
    {% if execute %}
      {{ log(table ~ ': ' ~ results.columns[0].values()[0] ~ ' rows', info=true) }}
    {% endif %}
  {% endfor %}
{% endmacro %}

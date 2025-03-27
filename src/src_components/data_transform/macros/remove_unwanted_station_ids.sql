{% macro remove_unwanted_station_ids(column_name) %}
    where {{ column_name }} not in ('Lab - NYC', 'SYS032') and {{ column_name }} is not Null
{% endmacro %}
{% macro format_date(column_name) %}
    (date_trunc('second',strptime({{ column_name }}, '%Y-%m-%d %H:%M:%S.%f')))
{% endmacro %}
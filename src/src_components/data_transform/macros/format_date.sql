{% macro format_date(column_name) %}
    (
        coalesce(
            date_trunc('second',try_strptime({{ column_name }}, '%Y-%m-%d %H:%M:%S.%f')),
            date_trunc('second',try_strptime({{ column_name }}, '%Y-%m-%d %H:%M:%S'))
        )
    )
{% endmacro %}
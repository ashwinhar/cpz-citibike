{% test validate_month(model, column_name, month_idx)%}
    select * 
    from {{ model }} 
    where month({{ column_name }}) != {{ month_idx }}
{% endtest %}
{% test validate_month(model, started_at_col, ended_at_col, month_idx)%}
    select * 
    from {{ model }} 
    where 
        month({{ started_at_col }}) != {{ month_idx }} and month({{ ended_at_col }}) != {{ month_idx }}
{% endtest %}
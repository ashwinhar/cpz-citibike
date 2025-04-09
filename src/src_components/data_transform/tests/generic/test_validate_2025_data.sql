{% test validate_2025_data(model) %}
    with cte as (
        select 
            count(*) as total_records
        from {{ model }} 
        where 
            year(started_at) = 2025 and
            start_station_id = '6822.09' and 
            end_station_id = '7020.02'
    )
    select * from cte where total_records != 381
    
{% endtest %}

{% test validate_2024_data(model) %}
    with cte as (
        select 
            count(*) as total_records
        from {{ model }} 
        where 
            year(started_at) = 2024 and
            start_station_id = '6822.09' and 
            end_station_id = '7020.02'
    )
    select * from cte where total_records != 1661
    
{% endtest %}

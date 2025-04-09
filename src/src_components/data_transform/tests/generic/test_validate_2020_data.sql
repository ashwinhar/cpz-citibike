{% test validate_2020_data(model) %}
    with cte as (
        select 
            count(*) as total_records
        from {{ model }} 
        where 
            year(started_at) = 2020 and
            start_station_id = '6822.09' and 
            end_station_id = '7020.09'
    )
    select * from cte where total_records != 3127
    
{% endtest %}

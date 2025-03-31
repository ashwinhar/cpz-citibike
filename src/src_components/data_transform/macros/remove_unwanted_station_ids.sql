{% macro remove_unwanted_station_ids() %}
    where 
        start_station_id not in ('Lab - NYC', 'SYS032') and 
        start_station_id is not Null and
        end_station_id not in ('Lab - NYC', 'SYS032') and 
        end_station_id is not Null
{% endmacro %}
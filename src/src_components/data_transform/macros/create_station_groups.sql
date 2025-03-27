{% macro create_station_groups(model, start_or_end) %}
    select 
        {{ start_or_end }}_station_name as citibike_station_name, 
        {{ start_or_end }}_station_id as citibike_station_id, 
        round({{ start_or_end }}_lat, 6) as station_latitude, 
        round({{ start_or_end }}_lng, 6) as station_longitude
    from {{ model }}
    group by
        {{ start_or_end }}_station_name, 
        {{ start_or_end }}_station_id, 
        round({{ start_or_end }}_lat, 6), 
        round({{ start_or_end }}_lng, 6) 
{% endmacro %}
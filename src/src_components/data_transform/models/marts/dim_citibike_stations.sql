with new_struct as (
    select
        citibike_station_name,
        citibike_station_id,
        {
            'station_latitude': station_latitude,
            'station_longitude': station_longitude
        } as lat_long_pair
    from station_geographies
),

selected_name as (
    select
        citibike_station_id,
        first(citibike_station_name) as citibike_station_name,
        mode(lat_long_pair) as lat_long_pair_mode
    from new_struct
    group by citibike_station_id
)

select
    sn.*,
    sic.in_cpz
from selected_name as sn
left join {{ ref('station_in_cpz') }} as sic on
    sn.citibike_station_id = sic.citibike_station_id

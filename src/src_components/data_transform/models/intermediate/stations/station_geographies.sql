with start_station_groups as (
    {{ create_station_groups('combined_years', 'start') }}
),

end_station_groups as (
    {{ create_station_groups('combined_years', 'end') }}
),

all_station_groups as (
    select * from start_station_groups
    union
    select * from end_station_groups
)

select
    citibike_station_name,
    citibike_station_id,
    station_latitude,
    station_longitude
from all_station_groups
group by
    citibike_station_name,
    citibike_station_id,
    station_latitude,
    station_longitude

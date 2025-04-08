with cte as (
    pivot {{ ref ("combined_years") }}
    on year(started_at), month(started_at)
    using count(*)
    group by start_station_id, rideable_type
)

select
    cte.start_station_id,
    s.citibike_station_name,
    s.in_cpz,
    cte.rideable_type,
    cte.* exclude (cte.start_station_id, cte.rideable_type)
from cte
inner join {{ ref('dim_citibike_stations') }} as s
    on
        cte.start_station_id = s.citibike_station_id
order by start_station_id

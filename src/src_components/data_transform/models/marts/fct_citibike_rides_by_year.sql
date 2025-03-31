with cte as (
    pivot combined_years
    on year(started_at)
    using count(*)
    group by start_station_id
)
select
    cte.start_station_id,
    s.citibike_station_name,
    s.in_cpz,
    cte.* exclude (cte.start_station_id) 
from cte 
inner join {{ ref('dim_citibike_stations') }} as s on
    cte.start_station_id = s.citibike_station_id
order by start_station_id
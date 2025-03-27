with cte as (
    pivot combined_years
    on year(started_at)
    using count(*)
    group by start_station_id, start_station_name
)
select * from cte 
order by start_station_id
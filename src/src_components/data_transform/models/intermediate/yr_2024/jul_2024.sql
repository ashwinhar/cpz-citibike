with cte as (
    select * exclude("Unnamed: 0") from {{ source('staging_2024', '202407_citibike_tripdata_1') }} 
    UNION ALL 
    select * exclude("Unnamed: 0") from {{ source('staging_2024', '202407_citibike_tripdata_2') }}
    UNION ALL 
    select * exclude("Unnamed: 0") from {{ source('staging_2024', '202407_citibike_tripdata_3') }}
    UNION ALL 
    select * exclude("Unnamed: 0") from {{ source('staging_2024', '202407_citibike_tripdata_4') }}
    UNION ALL 
    select * exclude("Unnamed: 0") from {{ source('staging_2024', '202407_citibike_tripdata_5') }}
)
select
    ride_id,
    rideable_type,
    {{ format_date('started_at') }} as started_at,
    {{ format_date('ended_at') }} as ended_at,
    start_station_name,
    start_station_id,
    end_station_name,
    end_station_id,
    start_lat,
    start_lng,
    end_lat,
    end_lng, 
    member_casual
from cte

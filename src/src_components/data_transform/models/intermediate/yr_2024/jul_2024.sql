select * exclude("Unnamed: 0") from {{ source('staging_2024', '202407_citibike_tripdata_1') }} 
UNION ALL 
select * exclude("Unnamed: 0") from {{ source('staging_2024', '202407_citibike_tripdata_2') }}
UNION ALL 
select * exclude("Unnamed: 0") from {{ source('staging_2024', '202407_citibike_tripdata_3') }}
UNION ALL 
select * exclude("Unnamed: 0") from {{ source('staging_2024', '202407_citibike_tripdata_4') }}
UNION ALL 
select * exclude("Unnamed: 0") from {{ source('staging_2024', '202407_citibike_tripdata_5') }}


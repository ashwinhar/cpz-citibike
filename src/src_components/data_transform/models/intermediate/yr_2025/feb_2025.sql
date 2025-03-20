select * from {{ source('staging_2025', '202502_citibike_tripdata_1') }} 
UNION ALL 
select * from {{ source('staging_2025', '202502_citibike_tripdata_2') }} 
UNION ALL
select * from {{ source('staging_2025', '202502_citibike_tripdata_3') }} 

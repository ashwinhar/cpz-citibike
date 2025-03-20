select * from 
{{ source('staging_2023', '202308_citibike_tripdata_1') }} 
UNION ALL 
select * from {{ source('staging_2023', '202308_citibike_tripdata_2') }}
UNION ALL 
select * from {{ source('staging_2023', '202308_citibike_tripdata_3') }}
UNION ALL 
select * from {{ source('staging_2023', '202308_citibike_tripdata_4') }}

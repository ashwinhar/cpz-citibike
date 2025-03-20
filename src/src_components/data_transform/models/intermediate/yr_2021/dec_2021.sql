select * from 
{{ source('staging_2021', '202112_citibike_tripdata_1') }} 
UNION ALL 
select * from {{ source('staging_2021', '202112_citibike_tripdata_2') }}

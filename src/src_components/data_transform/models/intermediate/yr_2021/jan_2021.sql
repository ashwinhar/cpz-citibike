select * from 
{{ source('staging_2021', '202101_citibike_tripdata_1') }} 
UNION ALL 
select * from {{ source('staging_2021', '202101_citibike_tripdata_2') }}

select * from 
{{ source('staging_2020', '202012_citibike_tripdata_1') }} 
UNION ALL 
select * from {{ source('staging_2020', '202012_citibike_tripdata_2') }}

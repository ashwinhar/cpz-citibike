select * from 
{{ source('staging_2020', '202002_citibike_tripdata_1') }} 
UNION ALL 
select * from {{ source('staging_2020', '202002_citibike_tripdata_2') }}

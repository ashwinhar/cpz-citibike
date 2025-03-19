select * from 
{{ source('staging_2020', '202011_citibike_tripdata_1') }} 
UNION ALL 
select * from {{ source('staging_2020', '202011_citibike_tripdata_2') }}

select * from 
{{ source('staging_2022', '202203_citibike_tripdata_1') }} 
UNION ALL 
select * from {{ source('staging_2022', '202203_citibike_tripdata_2') }}

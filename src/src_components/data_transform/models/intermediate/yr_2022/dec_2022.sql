select * from 
{{ source('staging_2022', '202212_citibike_tripdata_1') }} 
UNION ALL 
select * from {{ source('staging_2022', '202212_citibike_tripdata_2') }}

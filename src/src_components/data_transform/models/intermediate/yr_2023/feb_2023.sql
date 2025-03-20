select * from 
{{ source('staging_2023', '202302_citibike_tripdata_1') }} 
UNION ALL
select * from 
{{ source('staging_2023', '202302_citibike_tripdata_1') }} 

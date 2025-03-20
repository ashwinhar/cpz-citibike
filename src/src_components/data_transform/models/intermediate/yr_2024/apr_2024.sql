select * from 
{{ source('staging_2024', '202404_citibike_tripdata') }}

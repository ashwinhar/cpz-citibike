select * from 
{{ source('staging_2024', '202403_citibike_tripdata') }}
select * from 
{{ source('staging_2024', '202402_citibike_tripdata') }}
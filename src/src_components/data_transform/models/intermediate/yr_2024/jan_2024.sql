select * from 
{{ source('staging_2024', '202401_citibike_tripdata') }} 

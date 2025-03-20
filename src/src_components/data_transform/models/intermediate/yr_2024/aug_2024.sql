select * EXCLUDE(rideable_type_duplicate_column_name_1) from {{ source('staging_2024', '202408_citibike_tripdata_1') }} 
UNION ALL 
select * EXCLUDE(rideable_type_duplicate_column_name_1) from {{ source('staging_2024', '202408_citibike_tripdata_2') }}
UNION ALL 
select * EXCLUDE(rideable_type_duplicate_column_name_1) from {{ source('staging_2024', '202408_citibike_tripdata_3') }}
UNION ALL 
select * EXCLUDE(rideable_type_duplicate_column_name_1) from {{ source('staging_2024', '202408_citibike_tripdata_4') }}
UNION ALL 
select * EXCLUDE(rideable_type_duplicate_column_name_1) from {{ source('staging_2024', '202408_citibike_tripdata_5') }}

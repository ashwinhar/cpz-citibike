{% docs tbl_month_year_description %}
Combines data from all relevant staging files. Specifically if the table is mm_yyyy, this table will `UNION ALL` data from all staging tables matching YYYYMM_citibike_tripdata_x where x is the index of the file. It will also format the dates as datetime, and truncate precision to 'second'. 
{% enddocs %}

{% docs tbl_year_description %}
Combines data from all relevant month tables. For example `yr_2020` contains data from all tables matching `mmm_2020`. Year tables also use the macro `remove_unwanted_station_ids`. Read the macro documentation for more info. 
{% enddocs %}
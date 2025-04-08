{% docs tbl_dim_citibike_stations %}
In the raw CitiBike data, `station_id` often does not have a consistent `station_name`. This table lists all possible `station_id` values in the fact tables, and associates them with a single `station_name`. Furthermore, it defines whether the station is in the congestion pricing zone (as of March 31st, 2025) or not. To read more about how we determine whether a station is within the congestion pricing zone, read the docs for `station_in_cpz` in the `intermediate` folder. 
{% enddocs %}

{% docs tbl_fct_citibike_rides_by_ym %}
Pivoting data from `combined_years` on `year(started_at), month(started_at)`, grouping number of rides by `start_station_id` and `rideable_type`.
{% enddocs %}

{% docs col_YYYY_MM %}
Column showing number of rides for a particular year-month combination. Column format will either by YYYY_M or YYYY_MM.
{% enddocs %}
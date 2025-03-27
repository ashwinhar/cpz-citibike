{% docs macros_create_station_groups_description %}
Pass in either 'start' or 'end' to parameter `start_or_end`. The macro will create distinct groups of `<start_or_end>_station_id`, `<start_or_end>_station_name`, `<start_or_end>_station_latitude`, and `<start_or_end>_station_longitude`.  Additionally, it will round the latitude and longitude values to 6 decimal points to handle floating point errors. 
{% enddocs %}

{% docs macros_remove_unwanted_station_ids %}
As of March 2025, there are three `start_station_id` values that have inconsistent `start_station_name` values, as well as inconsistent `start_lat` and `start_lng`. To simplify determining whether a `start_station_id` falls in the Congestion Pricing Zone, it's easier to remove records with these values. The impact is small at around ~50K records. For context, `fct_citibike_rides` has ~160M records. So ultimately, across all data, about 0.0003% of records are removed.
{% enddocs %}
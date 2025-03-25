{% docs tbl_staging_XXXXXX_citibike_tripdata_X %}
A .csv file taken from the CitiBike website (https://s3.amazonaws.com/tripdata/index.html) as is. Describes CitiBike data in a given month (formatted as YYYYMM) in the title. 
{% enddocs %}

{% docs col_ride_id %}
Unique identifier for a ride
{% enddocs %}

{% docs col_rideable_type %}
An enum, describing whether the bike was electric or acoustic
{% enddocs %}

{% docs col_started_at %}
The timestamp for when the ride started, presumably in EST (but CitiBike does not provide a data dictionary, so this is conjecture). 
For a month-specific table, can belong to the previous month as long as `ended_at` is in the appropriate month. For example, in `jan_2025`, 
several records have `month(started_at) = 12` (December), but the `month(ended_at)` for those records is `1`.
{% enddocs %}

{% docs col_ended_at %}
The timestamp for when the ride started, presumably in EST (but CitiBike does not provide a data dictionary, so this is conjecture).
For a month-specific table, can belong to the following month as long as `started_at` is in the appropriate month. For example, in `may_2024`, 
several records have `month(ended_at) = 6` (June), but the `month(started_at)` for those records is `5`.
{% enddocs %}

{% docs col_start_station_name %}
The name of the station where the ride started, usually an intersection.
{% enddocs %}

{% docs col_start_station_id %}
Unique identifier for the starting station
{% enddocs %}

{% docs col_end_station_name %}
The name of the station where the ride ended, usually an intersection.
{% enddocs %}

{% docs col_end_station_id %}
Unique identifier for the starting station
{% enddocs %}

{% docs col_start_lat %}
Latitude of the starting station
{% enddocs %}

{% docs col_start_lng %}
Longitude of the starting station
{% enddocs %}

{% docs col_end_lat %}
Latitude of the ending station
{% enddocs %}

{% docs col_end_lng %}
Longitude of the ending station
{% enddocs %}

{% docs col_member_casual %}
An enum, describing whether the rider was a CitiBike member, or if they were a non-member (aka "casual")
{% enddocs %}
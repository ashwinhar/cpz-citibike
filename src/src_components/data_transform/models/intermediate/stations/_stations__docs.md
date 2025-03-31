{% docs tbl_station_geographies %}
In the raw data, a `station_id` is sometimes associated with multiple `station_name` values, and is always associated with multiple `latitude` and `longitude` pairs. This table shows all distinct combinations of `station_name`, `station_id`, `latitude`, and `longitude` that appear in the raw data, both from `start_station` and `end_station`. In other words, for a `station_id = 123`, this table will show you every `station_name` that appears for that `station_id` in the raw data, as well as every lat/long pair. 
{% enddocs %}

{% docs col_station_id %}
Unique identifier for a station, either appearing in `start_station_id` or `end_station_id` in raw data. 
{% enddocs %}

{% docs col_station_name %}
Name associated with `col_station_id`, usually an intersection. 
{% enddocs %}

{% docs col_station_latitude %}
Latitude part of a lat/long pair that appears in the raw data for the `col_station_id` and `col_station_name` pair. 
{% enddocs %}

{% docs col_station_longitude %}
Latitude part of a lat/long pair that appears in the raw data for the `col_station_id` and `col_station_name` pair. 
{% enddocs %}

{% docs col_in_cpz %}
A boolean indicating whether the station is in the CPZ (Congestion Pricing Zone) or not. 
{% enddocs %}

{% docs tbl_station_in_cpz %}
Each `citibike_station_id` in the raw data is associated with many lat/long pairs, sometimes thousands of them. In many cases, sometimes these lat/long pairs are *within* the CPZ, and sometimes they are *outside* of the CPZ. There is no data dictionary to reference, but perhaps the lat/long generated for a ride is for the *dock* within a station, rather than the centroid of the station itself. Of course, this doesn't account for 1000 distinct combinations, so it might be some combination of floating point errors and faulty data. 

Therefore, it isn't straightforward to determine whether a single `station_id` is within the CPZ or not. In order to make a decision whether `in_cpz = True` or `in_cpz = False`, we find whether the lat/long pairs **tend** to be one way or another. For example, if there are 1000 distinct lat/long pairs that appear for a single `station_id`, and 900 lat/long pairs fall within the CPZ and 100 do not, we mark that `station_id` as `in_cpz = True` (and vice versa). It's important to note that we make this decision **irrespective of data volume**. That is to say, any lat/long pair logged against a `station_id` counts *one time* in the decision for `in_cpz` irrespective of how many times it *actually* appears in the raw data. 

In the data analysis, each `station_id` usually has an extremely clear bias towards being within the CPZ or not. `station_id` values where the difference between the `in_cpz = True` lat/long pairs and `in_cpz = False` lat/long pairs is less than 100 are automatically set to `in_cpz = False`. 

The steps in the code below are: 
1. Select relevant columns from `station_geographies`
2. Use `utils.cpz_polygons` and the built-in DuckDB geography functions to determine whether a lat/long pair is within the polygon or not. Polygon was provided as a geojson by Transportation Alternatives, and is loaded using `load_geojson.ipynb`. 
3. Convert boolean values to "inside" and "outside" to avoid protected keywords in the pivot
4. Find how many times a lat/long pairs fall within the CPZ or outside of the CPZ for a given `station_id`
5. Pivot the data on `in_cpz` to make the subtraction easy
6. Use a `CASE` statement to determine the value for `in_cpz` for a `citibike_station_id`. Note that the threshold of "100" for the subtraction is arbitrary, and was selected by best judgement based on the data distribution. 


{% enddocs %}
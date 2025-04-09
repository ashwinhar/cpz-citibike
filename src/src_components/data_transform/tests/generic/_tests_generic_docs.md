{% docs test_validate_YYYY_data %}
This is a manual data check on the year indicated, counting records where `start_station_id = '6822.09'` and `end_station_id = '7020.09'`. The validation number was generated directly from raw data, applying `UNION` to all the staging tables for the relevant year. 
{% enddocs %}

{% docs test_validate_YYYY_data_V2 %}
This is a manual data check on the year indicated, counting records where `start_station_id = '6822.09'` and `end_station_id = '7020.02'`. The validation number was generated directly from raw data, applying `UNION` to all the staging tables for the relevant year. 
{% enddocs %}
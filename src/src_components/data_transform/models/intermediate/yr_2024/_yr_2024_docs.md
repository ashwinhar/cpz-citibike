{% docs may_2024_description %}
`may_2024` and `june_2024` have several duplicate records (`ride_id` is repeated). All those records have a `month(started_at) = 5` and `month(ended_at) = 6`. This table has filtered for `month(started_at) = 5` and `month(ended_at) = 5`. This transformation is not necessary on other month-specific tables, as they do not contain duplicate records.
{% enddocs %}
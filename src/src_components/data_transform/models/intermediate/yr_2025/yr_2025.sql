with cte as (
    select * from {{ref ("jan_2025")}}
    union all
    select * from {{ref ("feb_2025")}}
    union all 
    select * from {{ref ("mar_2025")}}
    union all
    select * from {{ref ("apr_2025")}}
    union all
    select * from {{ref ("may_2025")}}
)
select * from cte
{{ remove_unwanted_station_ids() }}

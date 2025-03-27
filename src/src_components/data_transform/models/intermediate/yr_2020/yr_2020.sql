with cte as (
    select * from {{ref ("jan_2020")}}
    UNION ALL
    select * from {{ref ("feb_2020")}}
    UNION ALL
    select * from {{ref ("mar_2020")}}
    UNION ALL
    select * from {{ref ("apr_2020")}}
    UNION ALL
    select * from {{ref ("may_2020")}}
    UNION ALL
    select * from {{ref ("jun_2020")}}
    UNION ALL
    select * from {{ref ("jul_2020")}}
    UNION ALL
    select * from {{ref ("aug_2020")}}
    UNION ALL
    select * from {{ref ("sep_2020")}}
    UNION ALL
    select * from {{ref ("oct_2020")}}
    UNION ALL
    select * from {{ref ("nov_2020")}}
    UNION ALL
    select * from {{ref ("dec_2020")}}
)
select * from cte
{{ remove_unwanted_station_ids('start_station_id')}}
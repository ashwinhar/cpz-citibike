with cte as (
    select * from {{ref ("jan_2021")}}
    UNION ALL
    select * from {{ref ("feb_2021")}}
    UNION ALL
    select * from {{ref ("mar_2021")}}
    UNION ALL
    select * from {{ref ("apr_2021")}}
    UNION ALL
    select * from {{ref ("may_2021")}}
    UNION ALL
    select * from {{ref ("jun_2021")}}
    UNION ALL
    select * from {{ref ("jul_2021")}}
    UNION ALL
    select * from {{ref ("aug_2021")}}
    UNION ALL
    select * from {{ref ("sep_2021")}}
    UNION ALL
    select * from {{ref ("oct_2021")}}
    UNION ALL
    select * from {{ref ("nov_2021")}}
    UNION ALL
    select * from {{ref ("dec_2021")}}
)
select * from cte
{{ remove_unwanted_station_ids('start_station_id')}}
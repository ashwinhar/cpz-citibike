with cte as (
    select * from {{ref ("jan_2022")}}
    UNION ALL
    select * from {{ref ("feb_2022")}}
    UNION ALL
    select * from {{ref ("mar_2022")}}
    UNION ALL
    select * from {{ref ("apr_2022")}}
    UNION ALL
    select * from {{ref ("may_2022")}}
    UNION ALL
    select * from {{ref ("jun_2022")}}
    UNION ALL
    select * from {{ref ("jul_2022")}}
    UNION ALL
    select * from {{ref ("aug_2022")}}
    UNION ALL
    select * from {{ref ("sep_2022")}}
    UNION ALL
    select * from {{ref ("oct_2022")}}
    UNION ALL
    select * from {{ref ("nov_2022")}}
    UNION ALL
    select * from {{ref ("dec_2022")}}
)
select * from cte
{{ remove_unwanted_station_ids() }}
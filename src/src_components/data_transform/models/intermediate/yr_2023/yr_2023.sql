with cte as (
    select * from {{ref ("jan_2023")}}
    UNION ALL
    select * from {{ref ("feb_2023")}}
    UNION ALL
    select * from {{ref ("mar_2023")}}
    UNION ALL
    select * from {{ref ("apr_2023")}}
    UNION ALL
    select * from {{ref ("may_2023")}}
    UNION ALL
    select * from {{ref ("jun_2023")}}
    UNION ALL
    select * from {{ref ("jul_2023")}}
    UNION ALL
    select * from {{ref ("aug_2023")}}
    UNION ALL
    select * from {{ref ("sep_2023")}}
    UNION ALL
    select * from {{ref ("oct_2023")}}
    UNION ALL
    select * from {{ref ("nov_2023")}}
    UNION ALL
    select * from {{ref ("dec_2023")}}
)
select * from cte
{{ remove_unwanted_station_ids() }}
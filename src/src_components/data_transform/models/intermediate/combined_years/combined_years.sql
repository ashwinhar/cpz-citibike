select * from {{ ref ("yr_2020") }}
union all
select * from {{ ref ("yr_2021") }}
union all
select * from {{ ref ("yr_2022") }}
union all
select * from {{ ref ("yr_2023") }}
union all
select * from {{ ref ("yr_2024") }}
union all
select * from {{ ref ("yr_2025") }}

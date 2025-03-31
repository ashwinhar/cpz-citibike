with selected_name as (
    select
        citibike_station_id,
        first(citibike_station_name)
    from {{ ref('station_geographies')}}
    group by citibike_station_id
)
select
    sn.*,
    sic.in_cpz
from selected_name as sn
left join {{ ref('station_in_cpz') }} as sic on
    sn.citibike_station_id = sic.citibike_station_id
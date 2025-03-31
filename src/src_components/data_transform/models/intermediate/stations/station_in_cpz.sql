with cte as (
    select
        citibike_station_name,
        citibike_station_id,
        station_latitude,
        station_longitude
    from {{ ref('station_geographies') }}
),

in_polygon as (
    select
        cte.*,
        exists(
            select 1
            from utils.cpz_polygons as poly
            where st_within(
                st_point(cte.station_longitude, cte.station_latitude),
                poly.geometry
            )
        ) as in_cpz
    from cte
),

converted as (
    select
        citibike_station_id,
        station_latitude,
        station_longitude,
        case
            when in_cpz is true then 'inside'
            else 'outside'
        end as in_cpz
    from in_polygon
),

find_spread as (
    select
        citibike_station_id,
        in_cpz,
        count(*) as count_instances
    from converted
    group by
        citibike_station_id,
        in_cpz
),

pivoted as (
    pivot find_spread
    on in_cpz in ('inside', 'outside')
    using coalesce(sum(count_instances), 0)
    group by citibike_station_id
)

select
    citibike_station_id,
    case
        when abs(subtract(inside, outside)) < 100 then false
        when
            abs(subtract(inside, outside)) >= 100 and inside > outside
            then true
        when
            abs(subtract(inside, outside)) >= 100 and inside < outside
            then false
    end as in_cpz
from pivoted

{{ config(materialized='table') }}

-- Date spine generated via dbt_utils.date_spine.
-- Provides a complete set of dates for use in reporting and gap analysis.

with spine as (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2018-01-01' as date)",
        end_date="cast('2018-12-31' as date)"
    ) }}
),

final as (
    select
        spine.date_day,
        extract(year from spine.date_day) as year,
        extract(month from spine.date_day) as month,
        extract(day from spine.date_day) as day_of_month,
        extract(dow from spine.date_day) as day_of_week
    from spine
)

select * from final

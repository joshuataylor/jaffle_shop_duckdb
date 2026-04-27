-- The raw customer source data should not contain duplicate IDs.
select
    id,
    count(*) as record_count
from {{ ref('raw_customers') }}
group by 1
having record_count > 1

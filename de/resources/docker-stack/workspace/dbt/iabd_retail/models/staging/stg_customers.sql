with fuente as (
    select * from {{ source('src_retail_db', 'customers') }}
)
select
    customer_id     as cliente_id,
    customer_fname  as nombre,
    customer_lname  as apellido,
    customer_email  as email,
    customer_city   as ciudad,
    customer_state  as provincia
from fuente

-- Limpieza mínima sobre lo que cargó dlt: renombrado y tipos.
select
    customer_id,
    customer_fname                          as nombre,
    customer_lname                          as apellido,
    customer_fname || ' ' || customer_lname as nombre_completo,
    customer_city                           as ciudad,
    customer_zipcode                        as codigo_postal
from {{ source('retail_raw', 'customers') }}

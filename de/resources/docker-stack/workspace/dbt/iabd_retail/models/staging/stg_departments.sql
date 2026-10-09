with fuente as (
    select * from {{ source('retail_db', 'departments') }}
)
select
    department_id    as departamento_id,
    department_name  as nombre
from fuente

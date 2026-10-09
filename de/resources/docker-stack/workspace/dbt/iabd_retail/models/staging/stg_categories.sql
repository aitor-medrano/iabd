with fuente as (
    select * from {{ source('retail_db', 'categories') }}
)
select
    category_id             as categoria_id,
    category_department_id  as departamento_id,
    category_name           as nombre
from fuente

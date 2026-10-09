with fuente as (
    select * from "retail_el"."raw"."departments"
)
select
    department_id    as departamento_id,
    department_name  as nombre
from fuente
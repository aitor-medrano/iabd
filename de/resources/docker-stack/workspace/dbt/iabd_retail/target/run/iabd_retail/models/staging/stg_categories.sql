
  
  create view "retail_el"."main"."stg_categories__dbt_tmp" as (
    with fuente as (
    select * from "retail_el"."raw"."categories"
)
select
    category_id             as categoria_id,
    category_department_id  as departamento_id,
    category_name           as nombre
from fuente
  );

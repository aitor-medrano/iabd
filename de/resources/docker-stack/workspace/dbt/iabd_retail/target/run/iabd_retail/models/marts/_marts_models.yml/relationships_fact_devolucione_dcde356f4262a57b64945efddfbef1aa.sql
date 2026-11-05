
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with child as (
    select fecha_id as from_field
    from "retail_el"."main"."fact_devoluciones"
    where fecha_id is not null
),

parent as (
    select fecha_id as to_field
    from "retail_el"."main"."dim_fecha"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null



  
  
      
    ) dbt_internal_test
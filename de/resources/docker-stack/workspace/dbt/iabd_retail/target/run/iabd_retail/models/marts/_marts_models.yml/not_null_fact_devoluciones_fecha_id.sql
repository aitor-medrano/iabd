
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select fecha_id
from "retail_el"."main"."fact_devoluciones"
where fecha_id is null



  
  
      
    ) dbt_internal_test

    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select linea_id
from "retail_el"."main"."fact_ventas"
where linea_id is null



  
  
      
    ) dbt_internal_test
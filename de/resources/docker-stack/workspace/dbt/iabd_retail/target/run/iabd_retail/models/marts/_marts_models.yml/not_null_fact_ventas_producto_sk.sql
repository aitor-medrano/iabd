
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select producto_sk
from "retail_el"."main"."fact_ventas"
where producto_sk is null



  
  
      
    ) dbt_internal_test
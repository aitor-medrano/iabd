
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  -- Devuelve los departamentos con una tasa de devolución imposible
select departamento, unidades_vendidas, unidades_devueltas, tasa_devolucion_pct
from "retail_el"."main"."tasa_devolucion_departamento"
where tasa_devolucion_pct < 0 or tasa_devolucion_pct > 100
  
  
      
    ) dbt_internal_test

    

    create  table
      "retail_el"."main"."ingresos_por_departamento__dbt_tmp"
  
    
    as (
      with ventas as (
    select * from "retail_el"."main"."int_ventas_enriquecidas"
)
select
    departamento,
    count(distinct pedido_id)   as pedidos,
    sum(cantidad)               as unidades,
    round(sum(importe), 2)      as ingresos
from ventas
group by departamento
order by ingresos desc
    );
    
  

    

    create  table
      "retail_el"."main"."fact_devoluciones__dbt_tmp"
  
    
    as (
      with devoluciones as (
    select * from "retail_el"."main"."stg_devoluciones"
),
producto as (
    select * from "retail_el"."main"."dim_producto"
)
select
    d.devolucion_id,
    d.linea_id,
    d.pedido_id,                                      -- dimensión degenerada
    coalesce(dp.producto_sk, -1)   as producto_sk,    -- dimensión conformada
    d.fecha                        as fecha_id,       -- dimensión conformada
    d.unidades,
    d.importe,
    d.motivo,
    d.canal
from devoluciones d
left join producto dp on dp.producto_id = d.producto_id
    );
    
  

  
  create view "retail_el"."main"."stg_devoluciones__dbt_tmp" as (
    with fuente as (
    select * from read_parquet('/workspace/lago/devoluciones.parquet')
)
select
    devolucion_id,
    linea_id,
    pedido_id,
    producto_id,
    cast(fecha_devolucion as date) as fecha,
    unidades_devueltas             as unidades,
    importe_devuelto               as importe,
    motivo,
    canal
from fuente
  );

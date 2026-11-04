with fuente as (
    select * from {{ source('src_lago', 'devoluciones') }}
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
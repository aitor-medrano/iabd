with lineas as (
    select * from "retail_el"."main"."stg_order_items"
),
pedidos as (
    select * from "retail_el"."main"."stg_orders"
),
producto as (
    select * from "retail_el"."main"."dim_producto"
),
cliente as (
    select * from "retail_el"."main"."dim_cliente"
)
select
    l.linea_id,
    p.pedido_id                      as pedido_id,       -- dimensión degenerada
    coalesce(dc.cliente_sk,  -1)     as cliente_sk,
    coalesce(dp.producto_sk, -1)     as producto_sk,
    p.fecha                          as fecha_id,
    p.estado,
    l.cantidad,                                          -- aditiva
    l.subtotal                       as importe,         -- aditiva
    l.precio_unitario                                    -- NO aditiva
from lineas l
join pedidos p on l.pedido_id = p.pedido_id
left join producto dp on dp.producto_id = l.producto_id
left join cliente  dc on dc.cliente_id  = p.cliente_id
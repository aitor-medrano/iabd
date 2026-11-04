-- Grano: una línea de pedido entregada.
-- Resuelve una sola vez el join con dim_producto y la regla de negocio
-- "sólo pedidos entregados", que necesitan los dos marts de departamento.
with ventas as (
    select * from {{ ref('fact_ventas') }}
),
producto as (
    select * from {{ ref('dim_producto') }}
)
select
    v.linea_id,
    v.pedido_id,
    v.producto_sk,
    dp.departamento,
    dp.categoria,
    v.fecha_id,
    v.cantidad,
    v.importe
from ventas v
join producto dp on dp.producto_sk = v.producto_sk
where v.estado in ('COMPLETE', 'CLOSED')
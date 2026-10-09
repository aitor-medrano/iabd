with ventas as (
    select * from "retail_el"."main"."fact_ventas"
),
producto as (
    select * from "retail_el"."main"."dim_producto"
)
select
    dp.departamento,
    count(distinct v.pedido_id)   as pedidos,
    sum(v.cantidad)               as unidades,
    round(sum(v.importe), 2)      as ingresos
from ventas v
join producto dp on dp.producto_sk = v.producto_sk
where v.estado in ('COMPLETE', 'CLOSED')
group by dp.departamento
order by ingresos desc
with v as (
    select departamento,
           sum(cantidad)            as unidades_vendidas,
           round(sum(importe), 2)   as ingresos
    from "retail_el"."main"."int_ventas_enriquecidas"
    group by departamento
),
d as (
    select dp.departamento,
           sum(fd.unidades)            as unidades_devueltas,
           round(sum(fd.importe), 2)   as importe_devuelto
    from "retail_el"."main"."fact_devoluciones" fd
    join "retail_el"."main"."dim_producto" dp on dp.producto_sk = fd.producto_sk
    group by dp.departamento
)
select
    v.departamento,
    v.unidades_vendidas,
    coalesce(d.unidades_devueltas, 0)   as unidades_devueltas,
    v.ingresos,
    coalesce(d.importe_devuelto, 0)     as importe_devuelto,
    round(100.0 * coalesce(d.unidades_devueltas, 0) / v.unidades_vendidas, 1) as tasa_devolucion_pct
from v
left join d on d.departamento = v.departamento
order by tasa_devolucion_pct desc
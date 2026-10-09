with limites as (
    select min(fecha) as desde, max(fecha) as hasta
    from {{ ref('stg_orders') }}
),
dias as (
    select unnest(range(
        (select desde from limites),
        (select hasta from limites) + interval 1 day,
        interval 1 day
    ))::date as fecha_id
)
select
    fecha_id,
    year(fecha_id)     as anio,
    quarter(fecha_id)  as trimestre,
    month(fecha_id)    as mes,
    ['enero','febrero','marzo','abril','mayo','junio','julio',
     'agosto','septiembre','octubre','noviembre','diciembre'][month(fecha_id)] as mes_nombre,
    isodow(fecha_id)   as dia_semana,
    ['lunes','martes','miércoles','jueves','viernes','sábado',
     'domingo'][isodow(fecha_id)] as dia_nombre,
    isodow(fecha_id) >= 6 as es_finde
from dias

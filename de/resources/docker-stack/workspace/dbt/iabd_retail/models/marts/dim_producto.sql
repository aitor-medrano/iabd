with productos as (
    select * from {{ ref('stg_products') }}
),
categorias as (
    select * from {{ ref('stg_categories') }}
),
departamentos as (
    select * from {{ ref('stg_departments') }}
),
base as (
    select
        row_number() over (order by p.producto_id)   as producto_sk,
        p.producto_id,
        p.nombre                                      as nombre,
        coalesce(c.nombre, '(sin asignar)')           as categoria,
        coalesce(d.nombre, '(sin asignar)')           as departamento,
        p.precio                                      as precio_catalogo
    from productos p
    left join categorias c    on p.categoria_id = c.categoria_id
    left join departamentos d on c.departamento_id = d.departamento_id
)
select * from base
union all
select -1, -1, '(desconocido)', '(desconocido)', '(desconocido)', 0   -- miembro desconocido

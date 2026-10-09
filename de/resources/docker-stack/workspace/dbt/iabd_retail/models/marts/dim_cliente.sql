with clientes as (
    select * from {{ ref('stg_customers') }}
),
base as (
    select
        row_number() over (order by cliente_id)   as cliente_sk,
        cliente_id,
        nombre || ' ' || apellido                 as nombre,
        ciudad,
        provincia
    from clientes
)
select * from base
union all
select -1, -1, '(desconocido)', '(desconocido)', '(desconocido)'   -- miembro desconocido

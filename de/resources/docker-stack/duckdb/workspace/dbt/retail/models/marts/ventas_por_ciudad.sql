-- Mart de negocio: se materializa como tabla (ver dbt_project.yml).
select
    c.ciudad,
    count(*)                     as pedidos,
    round(sum(o.importe), 2)     as importe_total,
    round(avg(o.importe), 2)     as ticket_medio
from {{ ref('stg_orders') }} o
join {{ ref('stg_customers') }} c using (customer_id)
where o.estado = 'COMPLETE'
group by c.ciudad
order by importe_total desc

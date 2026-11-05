
    
    

select
    pedido_id as unique_field,
    count(*) as n_records

from "retail_el"."main"."fact_ventas"
where pedido_id is not null
group by pedido_id
having count(*) > 1



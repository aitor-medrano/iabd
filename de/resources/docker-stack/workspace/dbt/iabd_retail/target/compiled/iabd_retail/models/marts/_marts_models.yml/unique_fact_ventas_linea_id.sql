
    
    

select
    linea_id as unique_field,
    count(*) as n_records

from "retail_el"."main"."fact_ventas"
where linea_id is not null
group by linea_id
having count(*) > 1



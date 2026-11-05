
    
    

with all_values as (

    select
        estado as value_field,
        count(*) as n_records

    from "retail_el"."main"."fact_ventas"
    group by estado

)

select *
from all_values
where value_field not in (
    'CANCELED','CLOSED','COMPLETE','ON_HOLD','PAYMENT_REVIEW','PENDING','PENDING_PAYMENT','PROCESSING','SUSPECTED_FRAUD'
)



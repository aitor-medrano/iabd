
  
  create view "retail_el"."main"."stg_orders__dbt_tmp" as (
    with fuente as (
    select * from "retail_el"."raw"."orders"
)
select
    order_id                   as pedido_id,
    cast(order_date as date)   as fecha,      -- dlt cargó la fecha como texto
    order_customer_id          as cliente_id,
    order_status               as estado
from fuente
  );

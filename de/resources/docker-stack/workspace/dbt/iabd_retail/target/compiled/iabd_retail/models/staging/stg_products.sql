with fuente as (
    select * from "retail_el"."raw"."products"
)
select
    product_id           as producto_id,
    product_category_id  as categoria_id,
    product_name         as nombre,
    product_price        as precio
from fuente
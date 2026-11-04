with fuente as (
    select * from {{ source('src_retail_db', 'products') }}
)
select
    product_id           as producto_id,
    product_category_id  as categoria_id,
    product_name         as nombre,
    product_price        as precio
from fuente

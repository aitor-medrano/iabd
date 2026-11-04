with fuente as (
    select * from {{ source('src_retail_db', 'order_items') }}
)
select
    order_item_id             as linea_id,
    order_item_order_id       as pedido_id,
    order_item_product_id     as producto_id,
    order_item_quantity       as cantidad,
    order_item_subtotal       as subtotal,
    order_item_product_price  as precio_unitario
from fuente

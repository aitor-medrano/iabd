select
    order_id,
    cast(order_date as date) as fecha,
    order_customer_id        as customer_id,
    order_status             as estado,
    cast(order_total as decimal(10, 2)) as importe
from {{ source('retail_raw', 'orders') }}

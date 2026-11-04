-- =============================================================================
-- Genera devoluciones.parquet a partir de retail_db (esquema raw).
-- Segunda fuente del proyecto dbt: llega como fichero, no como tabla.
--
-- Uso (crea antes la carpeta destino:  mkdir -p /workspace/lago):
--   duckdb /workspace/dbt/iabd/retail_el.duckdb < gen_devoluciones.sql
--
-- Es DETERMINISTA: usa hash() en lugar de random(), así que todo el mundo
-- obtiene exactamente las mismas devoluciones y las cifras son comparables.
-- =============================================================================

COPY (
    with entregadas as (
        -- Sólo se puede devolver lo que se entregó
        select
            oi.order_item_id,
            oi.order_item_order_id,
            oi.order_item_product_id,
            oi.order_item_quantity,
            oi.order_item_subtotal,
            o.order_date
        from raw.order_items oi
        join raw.orders o on o.order_id = oi.order_item_order_id
        where o.order_status in ('COMPLETE', 'CLOSED')
    ),
    marcadas as (
        -- ~12% de las líneas entregadas se devuelven
        select *, hash(order_item_id) as h
        from entregadas
        where hash(order_item_id) % 100 < 12
    )
    select
        row_number() over (order by order_item_id)                     as devolucion_id,
        order_item_id                                                  as linea_id,
        order_item_order_id                                            as pedido_id,
        order_item_product_id                                          as producto_id,
        (order_date + to_days((h % 28 + 3)::int))::date                as fecha_devolucion,
        least(order_item_quantity, (h % 3 + 1)::int)                   as unidades_devueltas,
        round(order_item_subtotal / order_item_quantity
              * least(order_item_quantity, (h % 3 + 1)::int), 2)       as importe_devuelto,
        ['talla incorrecta','defectuoso','no era lo esperado',
         'llegó tarde','cambio de opinión'][(h % 5 + 1)::int]          as motivo,
        ['tienda','mensajería','punto de recogida'][(h % 3 + 1)::int]  as canal
    from marcadas
    order by devolucion_id
) TO '/workspace/lago/devoluciones.parquet' (FORMAT PARQUET);

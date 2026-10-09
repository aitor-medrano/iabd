import pyarrow as pa
import pyarrow.parquet as pq

pedidos = pa.table({
    "order_id": [1, 2],
    "cliente": [{"nombre": "Aitor", "pais": "ES"},
                {"nombre": "Pedro", "pais": "FR"}],
    "lineas": [[{"sku": "A1", "uds": 2}, {"sku": "B7", "uds": 1}],
               [{"sku": "C3", "uds": 5}]],
})
pq.write_table(pedidos, "pedidos.parquet")

# ¿Cuántas columnas hay REALMENTE dentro del fichero?
pf = pq.ParquetFile("pedidos.parquet")
print(f"Columnas físicas: {pf.metadata.num_columns}")
for i in range(pf.metadata.row_group(0).num_columns):
    print("  " + pf.metadata.row_group(0).column(i).path_in_schema)

print(pq.read_table("pedidos.parquet", columns=["order_id", "cliente.nombre"]))
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.json as pajson

# 1.- Definimos el esquema
schema = pa.schema([('nombre', pa.string()),
                    ('altura', pa.int32()),
                    ('edad',   pa.int32())])

# 2.- Leemos los empleados forzando nuestro esquema
opciones = pajson.ParseOptions(explicit_schema=schema)
tabla = pajson.read_json("empleados.jsonl", parse_options=opciones)

# 3.- Persistimos la tabla en Parquet
pq.write_table(tabla, 'empleados-json.parquet')

# 4.- Leemos el fichero generado
print(pq.read_table('empleados-json.parquet'))
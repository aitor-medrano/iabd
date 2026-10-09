import pyarrow as pa
import pyarrow.parquet as pq

# 1.- Definimos el esquema
schema = pa.schema([('nombre', pa.string()),
                    ('altura', pa.int32()),
                    ('edad',   pa.int32())])

# 2.- Los empleados, almacenados por columnas
empleados = {"nombre": ["Aitor", "Pedro"],
                "altura": [182, 178],
                "edad":   [48, None]}

# 3.- Creamos una tabla Arrow y la persistimos mediante Parquet
tabla = pa.Table.from_pydict(empleados, schema)
pq.write_table(tabla, 'empleados.parquet')

# 4.- Leemos el fichero generado
print(pq.read_table('empleados.parquet'))
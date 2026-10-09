import fastavro
import json

# 1. Leemos el esquema desde el fichero .avsc
with open("empleado.avsc", "rb") as f:
    esquema = fastavro.parse_schema(json.load(f))

# 2. Los datos. Pedro no tiene edad: la unión ["null", "int"] lo permite
empleados = [{"nombre": "Aitor", "altura": 182, "edad": 48},
             {"nombre": "Pedro", "altura": 178}]

# 3. Persistimos. El esquema se escribe en la cabecera del fichero
with open("empleados.avro", "wb") as f:
    fastavro.writer(f, esquema, empleados)

# 4. Leemos. No hace falta el .avsc: el fichero ya lleva su esquema dentro
with open("empleados.avro", "rb") as f:
    lector = fastavro.reader(f)
    esquema_del_fichero = lector.writer_schema
    codec = lector.codec
    leidos = list(lector)

print(f"Esquema almacenado en el fichero:\n{json.dumps(esquema_del_fichero)}\n")
print(f"Codec de compresión: {codec}\n")
print(f"Empleados:\n{leidos}")

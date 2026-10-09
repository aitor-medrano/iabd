import fastavro

import fastavro

def leer_con(reader_schema):
    """Lee empleados.avro (escrito con el esquema v1) usando otro esquema"""
    with open("empleados.avro", "rb") as f:
        return list(fastavro.reader(f, reader_schema=reader_schema))
    
v2 = fastavro.parse_schema({
    "type": "record", "namespace": "SeveroOchoa", "name": "empleado",
    "fields": [
        {"name": "nombre", "type": "string"},
        {"name": "altura", "type": "int"},
        {"name": "edad", "type": ["null", "int"], "default": None},
        {"name": "departamento", "type": "string", "default": "Sin asignar"}
    ]})

print(leer_con(v2))

v2b = fastavro.parse_schema({
    "type": "record", "namespace": "SeveroOchoa", "name": "empleado",
    "fields": [
        {"name": "nombre", "type": "string"},
        {"name": "altura", "type": "int"},
        {"name": "edad", "type": ["null", "int"], "default": None},
        {"name": "departamento", "type": "string"}
    ]})

# print(leer_con(v2b))

v3 = fastavro.parse_schema({
    "type": "record", "namespace": "SeveroOchoa", "name": "empleado",
    "fields": [
        {"name": "nombre_completo", "type": "string", "aliases": ["nombre"]},
        {"name": "altura", "type": "int"},
        {"name": "edad", "type": ["null", "int"], "default": None}
    ]})

print(leer_con(v3))

v4 = fastavro.parse_schema({
    "type": "record", "namespace": "SeveroOchoa", "name": "empleado",
    "fields": [
        {"name": "nombre", "type": "string"},
        {"name": "altura", "type": "int"}
    ]})

print(leer_con(v4))
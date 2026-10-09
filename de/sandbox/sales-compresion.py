"""Compara el tamaño en disco del mismo dataset en distintos formatos y compresiones."""
import os, shutil
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.orc as orc
import fastavro
 
DIR = "comparativa"
shutil.rmtree(DIR, ignore_errors=True); os.makedirs(DIR)
 
# --------------------------------------------------------------- 1. Los datos
ORIGEN = "pdi_sales.csv"
print(f"Fichero de partida: {ORIGEN} · {os.path.getsize(ORIGEN)/1024**2:.2f} MiB")

df = pd.read_csv(ORIGEN, sep=";")
df["Zip"] = df["Zip"].str.strip()
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")

tabla = pa.Table.from_pandas(df, preserve_index=False)
print(f"{len(df)} filas · {len(df.columns)} columnas\n")

# ------------------------------------------------- 2. Escritores de cada formato
esquema_avro = fastavro.parse_schema({
    "name": "Sales", "namespace": "SeveroOchoa", "type": "record",
    "fields": [
        {"name": "ProductID", "type": "int"},
        {"name": "Date",      "type": {"type": "int", "logicalType": "date"}},
        {"name": "Zip",       "type": "string"},
        {"name": "Units",     "type": "int"},
        {"name": "Revenue",   "type": "float"},
        {"name": "Country",   "type": "string"},
    ]})
registros = df.assign(Date=df["Date"].dt.date).to_dict("records")
 
def avro(ruta, codec):
    with open(ruta, "wb") as f:
        fastavro.writer(f, esquema_avro, registros, codec=codec)
 
def arrow(ruta, compresion):
    opciones = pa.ipc.IpcWriteOptions(compression=compresion)
    with pa.OSFile(ruta, "wb") as sink:
        with pa.ipc.new_file(sink, tabla.schema, options=opciones) as w:
            w.write_table(tabla)
 
# ------------------------------------------------------- 3. Qué vamos a probar
pruebas = [
    ("CSV",     "ninguna",   "ventas.csv",            lambda r: df.to_csv(r, sep=";", index=False)),
    ("CSV",     "gzip",      "ventas.csv.gz",         lambda r: df.to_csv(r, sep=";", index=False, compression="gzip")),
    ("JSONL",   "ninguna",   "ventas.jsonl",          lambda r: df.to_json(r, orient="records", lines=True, date_format="iso")),
 
    ("Avro",    "ninguna",   "ventas.avro",           lambda r: avro(r, "null")),
    ("Avro",    "deflate",   "ventas-deflate.avro",   lambda r: avro(r, "deflate")),
    ("Avro",    "snappy",    "ventas-snappy.avro",    lambda r: avro(r, "snappy")),
    ("Avro",    "zstandard", "ventas-zstd.avro",      lambda r: avro(r, "zstandard")),
 
    ("Arrow",   "ninguna",   "ventas.arrow",          lambda r: arrow(r, None)),
    ("Arrow",   "zstd",      "ventas-zstd.arrow",     lambda r: arrow(r, "zstd")),
 
    ("Parquet", "ninguna",   "ventas.parquet",        lambda r: pq.write_table(tabla, r, compression="none")),
    ("Parquet", "snappy",    "ventas-snappy.parquet", lambda r: pq.write_table(tabla, r, compression="snappy")),
    ("Parquet", "gzip",      "ventas-gzip.parquet",   lambda r: pq.write_table(tabla, r, compression="gzip")),
    ("Parquet", "zstd",      "ventas-zstd.parquet",   lambda r: pq.write_table(tabla, r, compression="zstd")),
 
    ("ORC",     "ninguna",   "ventas.orc",            lambda r: orc.write_table(tabla, r, compression="uncompressed")),
    ("ORC",     "zlib",      "ventas-zlib.orc",       lambda r: orc.write_table(tabla, r, compression="zlib")),
    ("ORC",     "zstd",      "ventas-zstd.orc",       lambda r: orc.write_table(tabla, r, compression="zstd")),
]
 
# ------------------------------------------------------------- 4. Ejecución
resultados = []
for formato, compresion, fichero, escribe in pruebas:
    ruta = os.path.join(DIR, fichero)
    try:
        escribe(ruta)
        resultados.append((formato, compresion, fichero, os.path.getsize(ruta)))
    except Exception as e:
        print(f"  ! {formato} + {compresion} no disponible: {str(e)[:70]}")
 
# ------------------------------------------------------------ 5. Resultados
csv = next(t for f, c, _, t in resultados if f == "CSV" and c == "ninguna")
print(f"{'Formato':<9}{'Compresión':<12}{'Fichero':<24}{'Tamaño':>10}{'vs CSV':>9}")
print("-" * 64)
for formato, compresion, fichero, tam in resultados:
    print(f"{formato:<9}{compresion:<12}{fichero:<24}{tam/1024**2:>7.2f} MiB{csv/tam:>8.1f}x")
 
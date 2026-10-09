"""
Compara pandas / Polars (eager y lazy) / DuckDB sobre un CSV grande:
cuenta las filas con importe > 100 y mide TIEMPO y PICO DE MEMORIA (RAM).

Uso:
    python3 bench_motores.py            # lanza los 4 motores y muestra la tabla
    python3 bench_motores.py duckdb     # lanza solo uno (uso interno)

Cómo se mide la RAM:
    Se usa resource.getrusage(RUSAGE_SELF).ru_maxrss, que es el "pico" de
    memoria residente (RSS) del proceso: el máximo de RAM física que ha
    tenido en cualquier instante. Es un dato EXACTO que lleva el kernel
    (no un muestreo que pueda perderse el pico).

    IMPORTANTE:
    * Unidades de ru_maxrss: en Linux son KB; en macOS, bytes. El script
      lo ajusta según el sistema.
    * Cada motor se ejecuta en un PROCESO APARTE (el script se relanza a sí
      mismo con subprocess). Es imprescindible: ru_maxrss solo sube (es una
      marca de máximo), así que si midieras dos motores en el mismo proceso,
      el segundo heredaría el pico del primero.
    * El pico incluye el intérprete de Python + la librería importada + los
      datos. Por eso DuckDB marca ~120 MB y no casi cero: es la huella real
      del proceso, que es justo lo que decide si "cabe o no" en tu RAM.

Requisitos: pip install pandas polars duckdb   (numpy para generar el CSV)
El CSV 'ventas.csv' se genera con el snippet de los apuntes.
"""
import sys, time, resource, subprocess

FILE = "ventas.csv"

def peak_mb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1024 if sys.platform != "darwin" else r / 1024 / 1024

def pandas_():
    import pandas as pd
    df = pd.read_csv(FILE)                      # carga TODO en memoria
    return int((df["importe"] > 100).sum())

def polars_eager():
    import polars as pl
    df = pl.read_csv(FILE)                      # carga TODO (columnar, multihilo)
    return df.filter(pl.col("importe") > 100).height

def polars_lazy():
    import polars as pl
    lf = pl.scan_csv(FILE).filter(pl.col("importe") > 100).select(pl.len())
    try:
        return lf.collect(engine="streaming").item()   # Polars nuevo
    except TypeError:
        return lf.collect(streaming=True).item()         # Polars antiguo

def duckdb_():
    import duckdb
    return duckdb.sql(f"SELECT count(*) FROM '{FILE}' WHERE importe > 100").fetchone()[0]

ENGINES = {"pandas": pandas_, "polars-eager": polars_eager,
           "polars-lazy": polars_lazy, "duckdb": duckdb_}

if len(sys.argv) == 2 and sys.argv[1] in ENGINES:
    name = sys.argv[1]
    t0 = time.perf_counter()
    n = ENGINES[name]()
    dt = time.perf_counter() - t0
    print(f"{name}\t{n}\t{dt:.2f}\t{peak_mb():.0f}")
else:
    print(f"{'motor':13}{'filas>100':>12}{'tiempo(s)':>11}{'RAM pico(MB)':>14}")
    for name in ENGINES:
        out = subprocess.run([sys.executable, __file__, name], capture_output=True, text=True)
        nm, n, dt, mb = out.stdout.strip().split("\t")
        print(f"{nm:13}{int(n):>12,}{dt:>11}{mb:>14}")
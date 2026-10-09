import numpy as np, csv
rng = np.random.default_rng(42)
N = 15_000_000
cats  = np.array(["Ropa", "Calzado", "Deporte", "Hogar", "Electronica", "Juguetes"])
provs = np.array(["Alicante", "Valencia", "Madrid", "Barcelona", "Sevilla", "Murcia"])
base  = np.datetime64("2023-01-01")

with open("ventas.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["fecha", "tienda_id", "producto_id", "categoria", "provincia", "importe"])
    hecho = 0
    while hecho < N:
        n = min(1_000_000, N - hecho)
        fecha = (base + rng.integers(0, 730, n).astype("timedelta64[D]")).astype(str)
        w.writerows(zip(fecha,
                        rng.integers(1, 501, n),
                        rng.integers(1, 10001, n),
                        cats[rng.integers(0, len(cats), n)],
                        provs[rng.integers(0, len(provs), n)],
                        np.round(rng.gamma(2.0, 40.0, n), 2)))
        hecho += n